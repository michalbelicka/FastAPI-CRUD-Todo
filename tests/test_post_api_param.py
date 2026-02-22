import pytest
from fastapi.testclient import TestClient

# Add the project root to Python path so we can import `main.py` from tests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app

client = TestClient(app)

test_data = [
    # Happy path: all valid fields
    {
        "payload": {"title": "Valid basic task", "description": "Write the test", "status": "pending"},
        "expected": {"title": "Valid basic task", "description": "Write the test", "status": "pending"},
        "status_code": 200
    },
    # Happy path: all valid fields, non-standard status → API accepts any value
    {
        "payload": {"title": "Non-standard status", "description": "Write the code", "status": "banana"},
        "expected": {"title": "Non-standard status", "description": "Write the code", "status": "banana"},
        "status_code": 200
    },
    # Edge case: misspelled 'description' key → returns None and status code 200
    {
        "payload": {"title": "Misspelled description", "escription": "Another test", "status": "pending"},
        "expected": {"title": "Misspelled description", "description": None, "status": "pending"},
        "status_code": 200
    },
    # Edge case: missing description, non-standard status → returns None and status code 200
    {
        "payload": {"title": "Missing description with non-standard status", "status": "banana"},
        "expected": {"title": "Missing description with non-standard status", "description": None, "status": "banana"},
        "status_code": 200
    },
    # Edge case: missing 'description' key with standard status 'pending' → returns None and status code 200
    {
        "payload": {"title": "Missing description with default status", "status": "pending"},
        "expected": {"title": "Missing description with default status", "description": None, "status": "pending"},
        "status_code": 200
    },
    # Edge case: misspelled 'status' key → API sets it to default "pending" and returns status code 200
    {
        "payload": {"title": "Misspelled status", "description": "misspelled status", "statu": "banana"},
        "expected": {"title": "Misspelled status", "description": "misspelled status", "status": "pending"},
        "status_code": 200
    },
    # Edge case: missing 'status' key → API sets it to default "pending" and returns status code 200
    {
        "payload": {"title": "Missing status", "description": "missing status"},
        "expected": {"title": "Missing status", "description": "missing status", "status": "pending"},
        "status_code": 200
    },
    # Verify that providing an integer for 'title' results in status 200
    # and the value is returned as a string (automatic type conversion)
    {
        "payload": {"title": 123, "description": "int in title", "status": "pending"},
        "expected": {"title": "123", "description": "int in title", "status": "pending"},
        "status_code": 200
    },
    # Verify that providing a float for 'title' results in status 200
    # and the value is returned as a string (automatic type conversion)
    {
        "payload": {"title": 12.3, "description": "float in title", "status": "pending"},
        "expected": {"title": "12.3", "description": "float in title", "status": "pending"},
        "status_code": 200
    },
    # Verify that providing an integer for 'description' results in status 200
    # and the value is returned as a string (automatic type conversion)
    {
        "payload": {"title": "Int in description", "description": 123, "status": "pending"},
        "expected": {"title": "Int in description", "description": "123", "status": "pending"},
        "status_code": 200
    },
    # Verify that providing a float for 'description' results in status 200
    # and the value is returned as a string (automatic type conversion)
    {
        "payload": {"title": "Float in description", "description": 12.3, "status": "pending"},
        "expected": {"title": "Float in description", "description": "12.3", "status": "pending"},
        "status_code": 200
    },
    # Verify that providing an integer for 'title' and a float for 'description'
    # results in status 200, and both values are automatically converted to strings
    {
        "payload": {"title": 456, "description": 45.6, "status": "pending"},
        "expected": {"title": "456", "description": "45.6", "status": "pending"},
        "status_code": 200
    },
    # Verify that 'title', 'description', and 'status' accept strings containing special characters
    # (comma in title, dot in description, semicolon in status) and are treated as plain strings
    {
        "payload": {"title": "Comma, dot and semicolon", "description": "title. with comma", "status": "desc; with dot"},
        "expected": {"title": "Comma, dot and semicolon", "description": "title. with comma", "status": "desc; with dot"},
        "status_code": 200
    },
    # Verify that 'title', 'description', and 'status' accept strings representing
    # empty lists "[]" or empty dicts "{}" and return them unchanged with status 200
    {
        "payload": {"title": "{}", "description": "[]", "status": "{}"},
        "expected": {"title": "{}", "description": "[]", "status": "{}"},
        "status_code": 200
    },
    # Edge case: misspelled or missing 'title' key → API raises a validation error
    {
        "payload": {"titl": "Misspelled title", "description": "Misspelled title key", "status": "pending"},
        "expected": {
                    "detail": [
                        {
                            "loc": [
                                "body",
                                "title"
                            ],
                            "msg": "field required",
                            "type": "value_error.missing"
                        }
                    ]
                    },
        "status_code": 422
    },
    # Edge case: empty payload → API raises validation error for missing 'title' only
    {
        "payload": {},
        "expected": {
                    "detail": [
                        {
                            "loc": [
                                "body",
                                "title"
                            ],
                            "msg": "field required",
                            "type": "value_error.missing"
                        }
                    ]
                    },
        "status_code": 422
    },
    # Edge case: only 'title' provided → API sets 'description' to None and 'status' to default "pending"
    {
        "payload": {"title": "Only title"},
        "expected": {"title": "Only title", "description": None, "status": "pending"},
        "status_code": 200
    },
    # Edge case: 'title' is an empty list or dict → API raises a type error (behavior is the same for [] and {})
    {
        "payload": {"title": {}, "description": "empty dict in title", "status": "pending"},
        "expected": {
                    "detail": [
                        {
                            "loc": [
                                "body",
                                "title"
                            ],
                            "msg": "str type expected",
                            "type": "type_error.str"
                        }
                    ]
                    },
        "status_code": 422
    },
    # Edge case: 'description' is an empty list or dict → API raises a type error (behavior is the same for [] and {})
    {
        "payload": {"title": "Description is an empty list", "description": [], "status": "pending"},
        "expected": {
                    "detail": [
                        {
                            "loc": [
                                "body",
                                "description"
                            ],
                            "msg": "str type expected",
                            "type": "type_error.str"
                        }
                    ]
                    },
        "status_code": 422
    },
    # Edge case: 'status' is an empty list or dict → API raises a type error (behavior is the same for [] and {})
    {
        "payload": {"title": "Status is an empty dict", "description": "empty dict in status", "status": {}},
        "expected": {
                    "detail": [
                        {
                            "loc": [
                                "body",
                                "status"
                            ],
                            "msg": "str type expected",
                            "type": "type_error.str"
                        }
                    ]
                    },
        "status_code": 422
    },
    # Edge case: all fields ('title', 'description', 'status') are empty list or dict → API raises type errors for each field, indicating string type expected
    {
        "payload": {"title": {}, "description": [], "status": {}},
        "expected": {
                    "detail": [
                        {
                            "loc": [
                                "body",
                                "title"
                            ],
                            "msg": "str type expected",
                            "type": "type_error.str"
                        },
                        {
                            "loc": [
                                "body",
                                "description"
                            ],
                            "msg": "str type expected",
                            "type": "type_error.str"
                        },
                        {
                            "loc": [
                                "body",
                                "status"
                            ],
                            "msg": "str type expected",
                            "type": "type_error.str"
                        }
                    ]
                    },
        "status_code": 422
    }
]              

success_data = [case for case in test_data if case["status_code"] == 200]     
error_data = [case for case in test_data if case["status_code"] == 422]        

@pytest.mark.parametrize("test_case", success_data)
def test_create_todo_success(test_case):

    response = client.post("/todos", json=test_case["payload"])

    assert response.status_code == test_case["status_code"]

    todo_data = response.json()
    todo_id = todo_data.pop("id")

    assert isinstance(todo_id, int)
    assert todo_data == test_case["expected"]

    
@pytest.mark.parametrize("test_case", error_data)
def test_create_todo_validation_error(test_case):

    response = client.post("/todos", json=test_case["payload"])

    assert response.status_code == test_case["status_code"]
    assert response.json() == test_case["expected"]










    