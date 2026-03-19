import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app

client = TestClient(app)

@pytest.fixture
def create_todo():

    post_data = {
        "title": "string",
        "description": "string",
        "status": "pending"
    }

    response = client.post("/todos", json=post_data)

    assert response.status_code == 200
    assert "id" in response.json()

    todo_id = response.json()["id"]

    yield todo_id

    client.delete(f"/todos/{todo_id}")

def test_put_invalid_all_fields(create_todo):

    todo_id = create_todo

    put_data = {
        "title": [],
        "description": {},
        "status": {}
    }

    response = client.put(f"/todos/{todo_id}", json=put_data)
    assert response.status_code == 422
    
    response_json = response.json()
    
    assert "detail" in response_json

    for error in response_json["detail"]:
        loc = error["loc"][-1]
        msg = error["msg"]
        type = error["type"]

        assert loc in ["title", "description", "status"]
        assert msg == "str type expected"
        assert type == "type_error.str"

    