"""backend - FastAPI Application Entry Point."""

import logfire
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from scalar_fastapi import get_scalar_api_reference  # type: ignore

from src.configurations import configuration
from src.enums import Environment
from src.routes import auth_router, project_router

logfire.configure()

# TODO: Add Sentry integration for error tracking
# setup correctly .toml for use with pre-commit hooks

app = FastAPI(
    title=configuration.APP_NAME,
    description="API for backend",
    version="0.0.1",
    docs_url="/swagger"
    if configuration.ENVIRONMENT == Environment.DEVELOPMENT
    else None,
    redoc_url="/redoc"
    if configuration.ENVIRONMENT == Environment.DEVELOPMENT
    else None,
    openapi_url="/openapi.json"
    if configuration.ENVIRONMENT == Environment.DEVELOPMENT
    else None,
)

logfire.instrument_fastapi(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=configuration.CORS_ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "environment": configuration.ENVIRONMENT}


@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": f"Welcome to {configuration.APP_NAME}"}


for route in [auth_router, project_router]:
    app.include_router(route)


if configuration.ENVIRONMENT == Environment.DEVELOPMENT:

    @app.get("/docs", include_in_schema=False)
    async def scalar_docs() -> HTMLResponse:
        """Scalar API documentation."""
        return get_scalar_api_reference(
            openapi_url=app.openapi_url or "/openapi.json",
            title=app.title,
            hide_models=True,
        )
