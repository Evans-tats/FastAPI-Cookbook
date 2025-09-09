import csv
from typing import List,Optional
from models import Task, TaskWithID
DATABASE_FILE_NAME = "task.csv"

column_names = ["id", "title", "description", "status"]

def read_task_from_csv(task_id: int) -> Optional[TaskWithID]:
    try:
        with open(DATABASE_FILE_NAME, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row["id"]) == task_id:
                    return TaskWithID(
                        id=int(row["id"]),
                        title=row["title"],
                        description=row["description"],
                        status=row["status"]
                    )
    except FileNotFoundError:
        return {"detail": "File not found"}
    return None

def read_tasks_from_csv() -> List[TaskWithID]:
    tasks = []
    try:
        with open(DATABASE_FILE_NAME, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                task = TaskWithID(
                    id=int(row["id"]),
                    title=row["title"],
                    description=row["description"],
                    status=row["status"]
                )
                tasks.append(task)
    except FileNotFoundError:
        return {"detail": "File not found"}
    return tasks


from pathlib import Path


def write_task_to_csv(task: Task) -> TaskWithID:
    db_path = Path(DATABASE_FILE_NAME)

    # Ensure the file exists, create with header if not
    if not db_path.exists():
        with open(db_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=column_names)
            writer.writeheader()

    # Find the next available ID
    with open(db_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        ids = [int(row["id"]) for row in reader if row.get("id")]
        task_id = max(ids, default=0) + 1

    # Append the new task
    with open(db_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=column_names)
        writer.writerow({
            "id": task_id,
            "title": task.title,
            "description": task.description,
            "status": task.status
        })

    # Always return a TaskWithID model
    return TaskWithID(id=task_id, **task.model_dump())

    
def remove_task_from_csv(task_id: int) -> bool:
    try:
        tasks = read_tasks_from_csv()
        tasks = [task for task in tasks if task.id != task_id]
        with open(DATABASE_FILE_NAME, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=column_names)
            writer.writeheader()
            for task in tasks:
                writer.writerow({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status
                })
        return True
    except FileNotFoundError:
        return False