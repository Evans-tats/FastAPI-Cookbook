from fastapi import FastAPI, HTTPException, Depends
from models import Task, TaskWithID
from Operations import read_task_from_csv, read_tasks_from_csv,write_task_to_csv, remove_task_from_csv
from typing import Optional
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from models import Task, TaskWithID
import schema 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

schema.Base.metadata.create_all(engine)

@app.get("/tasks/{task_id}", response_model=TaskWithID)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(schema.Task).filter(schema.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
@app.get("/tasks", response_model=list[TaskWithID])
def get_tasks(status: Optional[str] = None, title: Optional[str] = None):
   
    tasks = read_tasks_from_csv()
    if status:
        tasks = [
            task for task in tasks if task.status.lower() == status.lower()
        ]
    if title:
        tasks = [
            task for task in tasks if title.lower() in task.title.lower()
        ]

    return tasks

@app.post("/task", response_model=TaskWithID)
def create_task(task: Task):
    new_task = write_task_to_csv(task)
    if isinstance(new_task, dict) and "detail" in new_task:
        raise HTTPException(status_code=500, detail=new_task["detail"])
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    success = remove_task_from_csv(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted successfully"}