import csv
import os
from pathlib import Path
from unittest.mock import patch
import pytest

TEST_DATABASE_FILE_NAME = 'test_task.csv'
TEST_TASK_CSV = [
    {
        "id": 1,
        "title": "Test Task One",
        "description": "Test Description One",
        "status": "Incomplete"
    },
    {
        "id": 2,
        "title": "Test Task Two",
        "description": "Test Description Two",
        "status": "Ongoing"
    }

]

TEST_TASK = [
    {**task_json, "id": int(task_json["id"])}
    for task_json in TEST_TASK_CSV
]

@pytest.fixture(autouse=True)
def create_test_database():
    database_file_location =str(Path(__file__).parent / TEST_DATABASE_FILE_NAME)
    with patch("Operations.DATABASE_FILE_NAME", database_file_location) as csv_test:
        with open ( database_file_location, mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames= ["id", "title", "description", "status"])
            writer.writeheader()
            writer.writerows(TEST_TASK_CSV)
            print("")
        yield csv_test
        if os.path.exists(database_file_location):
            os.remove(database_file_location)
