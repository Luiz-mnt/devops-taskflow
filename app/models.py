"""Contrato HTTP: status em inglês e títulos normalizados antes da persistência."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints

TaskTitle = Annotated[
    str,
    StringConstraints(
        strict=True,
        strip_whitespace=True,
        min_length=1,
        max_length=200,
        pattern=r"^[^\x00]+$",
    ),
]


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: TaskTitle


class TaskComplete(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Literal["completed"]


class TaskResponse(BaseModel):
    id: int
    title: str
    status: Literal["pending", "completed"]


class HealthResponse(BaseModel):
    status: Literal["healthy", "unhealthy"]
    database: Literal["ok", "unavailable"]
