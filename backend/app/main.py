"""FastAPI application entrypoint."""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.routers import employees

settings = get_settings()

app = FastAPI(
    title="Employee Directory Search API",
    description="Internal tool for searching and viewing employees.",
    version="1.0.0",
)

# CORS origins come from an environment variable (CORS_ORIGINS)
# rather than being hardcoded, so the same build works across
# local, dev, staging, and production environments.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(employees.router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Catch-all so unexpected errors never leak stack traces to clients."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred. Please try again later."
        },
    )


@app.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "ok"}