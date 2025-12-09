# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from fastapi import Query, Response
from fastapi.responses import StreamingResponse
from astroplan import Observer, FixedTarget, time_grid_from_range
from astropy.coordinates import EarthLocation
from astropy.time import Time
import astropy.units as u
import matplotlib.pyplot as plt
from matplotlib import cm
from io import BytesIO
import numpy as np
import pandas as pd


# Use absolute imports instead of relative ones
import app.database as database
# import app.models as models
# import app.schemas as schemas
# import app.crud as crud


from fastapi.middleware.cors import CORSMiddleware

# Get your Svelte frontend URL from an environment variable (best practice)
# Caddy's routing means the browser sees astro.vlousada.me

FRONTEND_URL = "http://astro.vlousada.me" # Use HTTPS if Caddy is fully set up for it



app = FastAPI(title="AstroPlanner API")


app.add_middleware(
    CORSMiddleware,
    # This must match your frontend domain exactly
    allow_origins=[FRONTEND_URL],
    # Crucial: Must be True to allow cookies/credentials to be sent
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static dashboard
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/images", StaticFiles(directory="app/static/images"), name="images")

#get url for static images  
my_static_url = f"{FRONTEND_URL}/static/images/"    
@app.get("/static_url")
def get_static_url():
    return {"static_url": my_static_url}


@app.get("/")
def root():
    return {"message": "AstroPlanner API is running"}


# Predefined observer (Lousada)
home_location = EarthLocation(lat=41.3*u.deg, lon=-8.5*u.deg, height=190*u.m)
observer = Observer(location=home_location, name="Lousada", timezone="Europe/Lisbon")



@app.get("/skyplot")
def skyplot(targets: list[str] = Query(...), start_time: str = Query(...)):
    """
    Generate sky plot for given targets and start_time (UTC string).
    Example:
    /skyplot?targets=M31&targets=M45&targets=M42&start_time=2025-12-04T21:00:00
    """

    # Compute time window
    t0 = Time(start_time)
    t1 = t0 + 10*u.hour
    time_grid = time_grid_from_range([t0, t1], time_resolution=1*u.hour)

    # Create targets
    fixed_targets = []
    for name in targets:
        try:
            fixed_targets.append(FixedTarget.from_name(name))
        except Exception as e:
            print(f"Warning: Could not resolve target {name}: {e}")

    # Create figure
    fig = plt.figure(figsize=(8, 8))
    cmap = cm.Set1

    for i, target in enumerate(fixed_targets):
        ax = plt.subplot(111, polar=True)
        from astroplan.plots import plot_sky
        plot_sky(
            target,
            observer,
            time_grid,
            style_kwargs=dict(color=cmap(float(i)/len(fixed_targets)), label=target.name),
            ax=ax
        )

    # Backyard obstruction mask (example placeholder)
    angles = np.linspace(0, 2*np.pi, 25)
    radii_sub = [63, 66, 63, 80, 82, 82, 81, 82, 83, 84, 85, 80,
                 60, 59, 55, 42, 20, 10, 10, 10, 15, 30, 42, 50, 63]
    ax.fill(angles, radii_sub, alpha=0.3, color='green')

    ax.set_theta_zero_location("S")
    ax.set_theta_direction(-1)
    ax.legend(loc="center right")

    # Return as PNG
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")







# --- retrieve astroTargets  from database as json ---
@app.get("/targets/all", tags=["Astro Targets"])
def get_astro_targets(db: Session = Depends(database.get_db)):
    res = {}
    kanban = {
        0:"Backlog",
        1:"Planning",
        2:"Starting",
        3:"Imaging",
        4:"Processing",
        5:"Reviewing",
        9:"Completed"
    }
    query = 'select * from astroTargets'
    if Session:
        df = pd.read_sql(query, con=database.engine)
        dfCols = []
        res['kanban'] = kanban
        if len(df):
            df = df.fillna('')  # replace NaN with empty string
            dfCols = list(df.columns)
            if 'type' in dfCols:
                df['type'] = df['type'].astype(str)
                df['type'] = df['type'].apply(lambda x: str(x).lower())
                res['types'] = df['type'].astype(str).unique().tolist()
            if 'subtype' in dfCols:
                df['subtype'] = df['subtype'].astype(str)
                df['subtype'] = df['subtype'].apply(lambda x: str(x).lower())  
                res['subtypes'] = df['subtype'].unique().tolist()
            
            res['targets'] = df.to_dict(orient='records')
        # return res as json
        return res
    else:
        raise HTTPException(status_code=500, detail="Database session not available")

# --- post new astroTarget to database with columns parameters---
@app.post("/targets/new", tags=["Astro Targets"])
def post_astro_target(dict_values, token, db: Session = Depends(database.get_db)):
    # Basic token check (replace with real authentication in production)
    if token != "fomalhaut7":
        raise HTTPException(status_code=401, detail="Invalid token")

    query = f"""INSERT INTO astroTargets (object, name, type, subtype, size, unit, best, gear, subs, integration, notes, image_file, kanban_step) 
                VALUES (
                '{dict_values.get("object", dict_values["object"])}',
                '{dict_values.get("name", dict_values["name"])}',
                '{dict_values.get("type", dict_values["type"])}',
                '{dict_values.get("subtype", dict_values["subtype"])}',
                '{dict_values.get("size", dict_values["size"])}',
                '{dict_values.get("unit", dict_values["unit"])}',
                '{dict_values.get("best", dict_values["best"])}',
                '{dict_values.get("gear", dict_values["gear"])}',
                '{dict_values.get("subs", dict_values["subs"])}',
                '{dict_values.get("integration", dict_values["integration"])}',
                '{dict_values.get("notes", dict_values["notes"])}',
                '{dict_values.get("image_file", dict_values["image_file"])}',
                {dict_values.get("kanban_step", dict_values["kanban_step"])}
            );"""
    try:
        with db.begin():
            db.execute(query)
        return {"message": "New astro target added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding new target: {e}")


# --- serve static images from astroTargets pngs---
@app.get("/targets/image/{image_file}", tags=["Astro Targets"])
def get_astro_target_image(image_file: str):
    image_path = f"app/static/images/{image_file}"
    try:
        with open(image_path, "rb") as image:
            return Response(content=image.read(), media_type="image/png")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Image not found")

# --- get top 10 targets for atual best month ---
@app.get("/targets/bestmonth/{bestmonth}", tags=["Astro Targets"])
def get_astro_targets_best_month(bestmonth: str, db: Session = Depends(database.get_db)):
    mesX = str(bestmonth)
    dict_months = {
        '1': "jan", '2': "feb", '3': "mar", '4': "apr", '5': "may", '6': "jun",
        '7': "jul", '8': "aug", '9': "sep", '10': "oct", '11': "nov", '12': "dec"
    }
    res = {}
    str_month = dict_months[mesX] if mesX in dict_months else 'jan'
    # query to get top 10 targets for the specified month

    query = f"""SELECT * FROM astroTargets 
                WHERE best LIKE '%%{str_month}%%' 
                ORDER BY FIELD(kanban_step, 2,3, 0,1,4,5, 9) ASC, 
                         FIELD(type, 'nebula', 'planetary', 'cluster', 'galaxy',  'other') ASC
                LIMIT 10;"""
    if Session:
        df = pd.read_sql(query, con=database.engine)
        dfCols = []
        if len(df):
            df = df.fillna('')
            res['targets'] = df.to_dict(orient='records')
            res['info'] = f"Top 10 targets for month: {str_month}"
        else:
            res['targets'] = []
            res['info'] = f"No targets found for the specified month: {str_month}"
        return res 
    else:
        raise HTTPException(status_code=500, detail="Database session not available")
