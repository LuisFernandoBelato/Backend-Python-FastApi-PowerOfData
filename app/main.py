from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.interfaces.controls.films.films_controller import router as films_router
from app.interfaces.controls.people.people_controller import router as people_router
from app.interfaces.controls.planets.planets_controller import router as planets_router
from app.interfaces.controls.species.species_controller import router as species_router
from app.interfaces.controls.starships.starships_controller import router as starships_router
from app.interfaces.controls.vehicles.vehicles_controller import router as vehicles_router

import os

app = FastAPI(
    title="Api Star Wars - Backend Python FastAPI",
    description="Arquitetura DDD: camada de API, domínio e infraestrutura comunicando com a SWAPI.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(films_router)
app.include_router(people_router)
app.include_router(planets_router)
app.include_router(species_router)
app.include_router(starships_router)
app.include_router(vehicles_router)

@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False, 
    )
