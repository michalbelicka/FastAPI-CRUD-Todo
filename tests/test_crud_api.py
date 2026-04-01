import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database.database import get_db
from models.models import TodoItem

from main import app

client = TestClient(app)

test_data = {
    "title": "task",
    "description": "create todo",
    "status": "pending"
}

@pytest.fixture(scope="module")
def create_todo():
    response = client.post("/todos", json=test_data)
    assert response.status_code == 200
    assert "id" in response.json()

    todo_id = response.json()["id"]
    assert isinstance(todo_id, int)
    return todo_id

def test_get_and_valid_update_todo(client, create_todo):

    todo_id = create_todo

    valid_update_data = {
        "title": "valid update",
        "description": "valid data",
        "status": "pending"
    }

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200

    todo_json = response.json()

    assert todo_json["title"] == "task"
    assert todo_json["description"] == "create todo"
    assert todo_json["status"] == "pending"

    response = client.put(f"/todos/{todo_id}", json=valid_update_data)
    assert response.status_code == 200

    get_response = client.get(f"/todos/{todo_id}")
    updated_data = get_response.json()
    
    assert "id" in updated_data
    assert updated_data["title"] == "valid update"
    assert updated_data["description"] == "valid data"
    assert updated_data["status"] == "pending"

    assert isinstance(updated_data["title"], str)
    assert isinstance(updated_data["description"], str)
    assert isinstance(updated_data["status"], str)
    assert isinstance(updated_data["id"], int)

def test_check_db_after_put(client, db: Session, create_todo):

    todo_id = create_todo
    
    todo_in_db = db.query(TodoItem).filter(TodoItem.id == todo_id).first()

    assert todo_in_db is not None

    assert todo_in_db.title == "valid update"
    assert todo_in_db.description == "valid data"
    assert todo_in_db.status == "pending"
   

def test_delete_todo(create_todo):

    todo_id = create_todo

    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200

    deleted_todo = response.json()
    assert "detail" in deleted_todo
    assert deleted_todo["detail"] == "Todo deleted"
    assert isinstance(deleted_todo["detail"], str)

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404

    deleted_data = response.json()

    assert "detail" in deleted_data
    assert deleted_data["detail"] == "Todo not found"
    assert isinstance(deleted_data["detail"], str)

def test_check_db_after_delete(db: Session, create_todo):

    todo_id = create_todo

    todo_in_db = db.query(TodoItem).filter(TodoItem.id == todo_id).first()

    assert todo_in_db is None


