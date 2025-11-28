from pydantic import Field, BaseModel
from typing import Optional

from api.models import TaskStatus

class TaskQuerySchema(BaseModel):
    project: Optional[str] = Field(None, max_length=80)
    name : Optional[str] = Field(None, max_length=80)
    status: Optional[TaskStatus] = None
    created_by_id: Optional[int] = None
    assigned_to_id: Optional[int] = None

class TaskCreateSchema(BaseModel):
    project: str = Field(..., max_length=80)
    name : str = Field(..., max_length=80)
    status: Optional[TaskStatus] = TaskStatus.NEW
    assigned_to_id: Optional[int] = None

    class Config:
        extra = "forbid"

class TaskUpdateSchema(BaseModel):
    project: Optional[str] = Field(None, max_length=80)
    name : Optional[str] = Field(None, max_length=80)
    status: Optional[TaskStatus]  = None
    assigned_to_id: Optional[int] = None

    class Config:
        extra = "forbid"