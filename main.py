"""A minimal FastAPI weather service wired to the golden path.

    GET /healthz          liveness/readiness probe (used by Kubernetes)
    GET /weather?city=    a dummy, deterministic "forecast" for a city

Deliberately dependency-free — there is no upstream weather API. The point of
this repo is the paved road around it (CI, scanning, keyless signing, SBOM, SLSA
provenance, GitOps), not the business logic. Kept trivial on purpose.
"""

import os

import uvicorn
from fastapi import FastAPI, Query

app = FastAPI(title="weather-api")

# A fixed set of conditions; a city maps to one deterministically so the response
# is stable and unit-testable without any network call.
_CONDITIONS = ("sunny", "cloudy", "rainy", "windy", "stormy")


def forecast_for(city: str) -> dict:
    """Pure, deterministic forecast for a city name. Same input -> same output."""
    key = city.strip().lower() or "nowhere"
    seed = sum(ord(c) for c in key)
    return {
        "city": key,
        "condition": _CONDITIONS[seed % len(_CONDITIONS)],
        "temperature_c": 15 + (seed % 20),  # 15..34, deterministic
    }


@app.get("/healthz")
async def healthz():
    """Liveness probe. Deliberately dependency-free."""
    return {"status": "ok"}


@app.get("/weather")
async def weather(city: str = Query(default="jakarta")):
    """Demo endpoint. Returns a deterministic forecast; city defaults to jakarta."""
    return forecast_for(city)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
