from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.api.routes import api_router
from app.core.config import get_settings
from app.db.session import Base, engine


settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="API FastAPI/PostgreSQL pour le suivi clinique en rhinologie.",
    )

    @app.on_event("startup")
    def on_startup() -> None:
        Base.metadata.create_all(bind=engine)

    @app.get("/health", tags=["system"])
    def health_check():
        return {"status": "ok", "environment": settings.environment}

    @app.get("/", include_in_schema=False)
    def root():
        return RedirectResponse(url="/api/v1/statistics/graphs")

    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()
