from sqlalchemy import Column, Integer, String, Date, DateTime, Enum
from datetime import datetime
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="pending")  # pending/completed
    due_date = Column(Date)
    created_at = Column(DateTime, default=datetime.now())
    priority = Column(String, default="medium")  # low/medium/high