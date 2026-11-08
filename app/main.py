"""Factory ASGI sem criar banco durante a importação."""

import os
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException
from fastapi import Path as PathParameter
from fastapi.responses import JSONResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.database import TaskStore
from app.models import HealthResponse, TaskComplete, TaskCreate, TaskResponse
from app.observability import HttpMetrics, ObservabilityMiddleware


def create_app(database_path: str | Path | None = None) -> FastAPI:
    configured_path = Path(
        database_path
        if database_path is not None
        else os.environ.get("TASKFLOW_DB_PATH", "data/taskflow.db")
    )
    store = TaskStore(configured_path)
    metrics = HttpMetrics()

    @asynccontextmanager
    async def lifespan(application: FastAPI):
        store.initialize()
        yield

    application = FastAPI(
        title="TaskFlow API",
        version="2.0.0",
        description="API acadêmica de tarefas com CI/CD e observabilidade.",
        lifespan=lifespan,
    )
    application.state.store = store
    application.state.metrics = metrics
    application.add_middleware(ObservabilityMiddleware, metrics=metrics)

    @application.post("/tasks", response_model=TaskResponse, status_code=201)
    def create_task(payload: TaskCreate):
        return store.create(payload.title)

    @application.get("/tasks", response_model=list[TaskResponse])
    def list_tasks():
        return store.list_all()

    @application.patch(
        "/tasks/{task_id}",
        response_model=TaskResponse,
        responses={404: {"description": "Tarefa inexistente"}},
    )
    def complete_task(
        task_id: Annotated[int, PathParameter(gt=0, le=9223372036854775807)],
        payload: TaskComplete,
    ):
        task = store.complete(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    @application.get(
        "/health",
        response_model=HealthResponse,
        responses={503: {"model": HealthResponse, "description": "Banco indisponível"}},
    )
    def health():
        try:
            store.check_health()
        except sqlite3.Error:
            return JSONResponse(
                status_code=503,
                content={"status": "unhealthy", "database": "unavailable"},
            )
        return {"status": "healthy", "database": "ok"}

    @application.get("/metrics", include_in_schema=False)
    def prometheus_metrics():
        return Response(
            generate_latest(metrics.registry), media_type=CONTENT_TYPE_LATEST
        )

    return application


app = create_app()
