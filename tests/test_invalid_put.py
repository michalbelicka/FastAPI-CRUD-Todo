import pytest
from fastapi.testclient import TestClient
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app

client = TestClient(app)

def test_invalid_update_wrong_id():
    
    fake_id = random.randint(1111111, 9999999)

    put_data = {
            "title": "string",
            "description": "string",
            "status": "string"      
            }
    
    response = client.put(f"/todos/{fake_id}", json=put_data)

    assert response.status_code == 404
    response_json = response.json()

    assert "detail" in response_json
    assert response_json["detail"] == "Todo not found"
    assert isinstance(response_json["detail"], str)


@pytest.fixture(scope="module")
def create_todo():

    post_data = {
        "title": "post data",
        "description": "post data",
        "status": "pending"
    }

    response = client.post("/todos", json=post_data)

    assert response.status_code == 200
    assert "id" in response.json()

    todo_id = response.json()["id"]
    return todo_id

def test_invalid_update_no_data(create_todo):

    todo_id = create_todo

    response = client.put(f"/todos/{todo_id}")
    assert response.status_code == 422

    response_json = response.json()

    assert "detail" in response_json
    assert isinstance(response_json["detail"], list)

    detail = response_json["detail"][0]
    assert isinstance(detail, dict)

    assert "body" in detail["loc"]
    assert isinstance(detail["loc"], list)

    assert detail["msg"] == "field required"
    assert isinstance(detail["msg"], str)

    assert detail["type"] == "value_error.missing"
    assert isinstance(detail["type"], str)
