from main import app
from fastapi.testclient import TestClient
from Operations import read_tasks_from_csv
from conftest import TEST_TASK

client = TestClient(app)

def test_endpoint_read_all_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == TEST_TASK

def test_endpoint_read_single_task():
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json() == TEST_TASK[0]
    response = client.get("/tasks/999")
    assert response.status_code == 404

def test_endpoint_create_task():
    task = {
        'title': 'New Task',
        'description': 'New Description',
        'status': 'Incomplete'
    }
    response = client.post('/task', json=task)
    assert response.status_code == 200
    assert response.json()['title'] == task['title']
    assert len(read_tasks_from_csv()) == 3

def test_endpoint_delete_task():
    response = client.delete('tasks/1')
    assert response.status_code == 200
    assert response.json() == {"detail": "Task deleted successfully"}
    assert len(read_tasks_from_csv()) == 1
