from unittest.mock import patch
from api.logic import MOCK_TASKS_LIST

# def test_get_tasks2(client):
#     # Mock return value: (response_dict, status_code)
#     mock_response = ({"tasks": ["task1", "task2"]}, 200)

#     with patch("api.logic.TaskLogic.get_tasks", return_value=mock_response):
#         resp = client.get("/get_tasks")

#     assert resp.status_code == 200
#     assert resp.get_json() == {"tasks": ["task1", "task2"]}

def test_get_tasks(client):
    rv = client.get("/get_tasks")
    
    assert rv.status_code == 200
    assert rv.json == MOCK_TASKS_LIST


def test_get_task(client):
    mock_response = ({"id": 1, "task": "Do something"}, 200)

    with patch("api.logic.TaskLogic.get_task", return_value=mock_response):
        resp = client.get("/get_task?id=1")

    assert resp.status_code == 200
    assert resp.get_json() == {"id": 1, "task": "Do something"}