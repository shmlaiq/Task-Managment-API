"""Task Management API - FastAPI Application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from app.database import engine
from app.routers.tasks import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - create tables on startup."""
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="Task Management API",
    description="A RESTful API for managing tasks with full CRUD operations",
    version="1.0.0",
    lifespan=lifespan,
)

# Include routers
app.include_router(tasks_router)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Task Management API",
        "docs": "/docs",
        "health": "/health"
    }
