from pydantic import BaseModel, validator
from datetime import date, datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    due_date: Optional[date] = None
    priority: Optional[str] = "medium"

    @validator('status')
    def validate_status(cls, v):
        if v not in ["pending", "completed"]:
            raise ValueError('Status must be either "pending" or "completed"')
        return v

    @validator('priority')
    def validate_priority(cls, v):
        if v not in ["low", "medium", "high"]:
            raise ValueError('Priority must be either "low", "medium", or "high"')
        return v

    @validator('due_date')
    def validate_due_date(cls, v, values):
        if v and 'created_at' in values and v < values['created_at'].date():
            raise ValueError('Due date cannot be before creation date')
        return v

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True