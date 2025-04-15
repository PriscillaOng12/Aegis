from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, symptoms, risk, wearables, interventions, analytics
from .telemetry import setup_tracing
from .services.db import init_db, close_db


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="Aegis Health API", version="1.0.0")

    # CORS configuration for local dev; restrict in production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Setup tracing
    setup_tracing(app)

    # Include routers
    app.include_router(auth.router, prefix="/v1", tags=["auth"])
    app.include_router(symptoms.router, prefix="/v1", tags=["symptoms"])
    app.include_router(risk.router, prefix="/v1", tags=["risk"])
    app.include_router(wearables.router, prefix="/v1", tags=["wearables"])
    app.include_router(interventions.router, prefix="/v1", tags=["interventions"])
    app.include_router(analytics.router, prefix="/v1", tags=["analytics"])

    @app.on_event("startup")
    async def on_startup() -> None:
        await init_db()

    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        await close_db()

    return app


app = create_app()