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


# Use absolute imports instead of relative ones
import app.database as database
import app.models as models
import app.schemas as schemas
import app.crud as crud


from fastapi.middleware.cors import CORSMiddleware

# Get your Svelte frontend URL from an environment variable (best practice)
# Caddy's routing means the browser sees astro.vlousada.me
FRONTEND_URL = "http://astro.vlousada.me" # Use HTTPS if Caddy is fully set up for it





models.Base.metadata.create_all(bind=database.engine)


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

@app.get("/")
def root():
    return {"message": "AstroPlanner API is running"}


# Predefined observer (Lousada)
home_location = EarthLocation(lat=41.3*u.deg, lon=-8.5*u.deg, height=190*u.m)
observer = Observer(location=home_location, name="Lousada", timezone="UTC")


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








# --- USERS ---
@app.post("/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    return crud.create_user(db, user)

# --- OBSERVATIONS ---
@app.post("/observations")
def create_observation(obs: schemas.ObservationCreate, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == obs.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_observation(db, obs)







from fastapi import APIRouter, Response, Depends, HTTPException
# (Your token generation logic goes here, e.g., creating a JWT)

@app.post("/login")
async def login(username: str, password: str, response: Response):
    # 1. Authenticate user against your database
    if not authenticate_user(username, password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # 2. Generate a session token (e.g., JWT)
    session_token = create_access_token({"sub": username})

    # 3. Set the HTTP-Only cookie
    response.set_cookie(
        key="session_id",
        value=session_token,
        # IMPORTANT SECURITY SETTINGS
        httponly=True,       # Prevents client-side JS access
        secure=True,         # Ensures cookie is only sent over HTTPS (if Caddy is active)
        samesite="lax",      # Good default protection against CSRF
        max_age=3600 * 24,   # 24 hours expiration
        path="/"             # Cookie valid for the entire domain
    )
    return {"message": "Login successful"}

# C. Protected Endpoint to Read Cookie

from fastapi import Cookie

def verify_session_cookie(session_id: str = Cookie(None)):
    if session_id is None or not is_valid_token(session_id):
        raise HTTPException(status_code=401, detail="Not authenticated")
    # Return user data or ID if successful
    return get_user_from_token(session_id)


@app.get("/user/me")
async def read_current_user(current_user: dict = Depends(verify_session_cookie)):
    return current_user