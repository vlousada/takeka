# app/main.py
from fastapi import FastAPI, Query, Response
from fastapi.responses import StreamingResponse
from astroplan import Observer, FixedTarget, time_grid_from_range
from astropy.coordinates import EarthLocation
from astropy.time import Time
import astropy.units as u
import matplotlib.pyplot as plt
from matplotlib import cm
from io import BytesIO
import numpy as np

app = FastAPI(title="AstroPlanner API")

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
