from sqlalchemy.orm import Session
import models, schemas
from datetime import date

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: schemas.TaskCreate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        for key, value in task.dict().items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

def get_tasks_by_status(db: Session, status: str):
    return db.query(models.Task).filter(models.Task.status == status).all()

def get_tasks_by_due_date(db: Session, due_date: date):
    return db.query(models.Task).filter(models.Task.due_date == due_date).all()

def search_tasks(db: Session, search_term: str):
    return db.query(models.Task).filter(
        (models.Task.title.contains(search_term)) | 
        (models.Task.description.contains(search_term))
    ).all()