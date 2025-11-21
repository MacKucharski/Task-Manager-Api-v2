# routes related to Task objects

from api import api
from api.logic import TaskLogic
from flask import request

@api.route("/api/tasks/<int:id>", methods = ["GET"])
def get_task(id):
    """Retrieve a task by id"""
    response, status = TaskLogic.get_task(id)
    return response, status

@api.route("/api/tasks", methods = ["GET"])
def get_tasks():
    """Retrieve list of tasks by query params"""
    params = request.args.to_dict()
    response, status = TaskLogic.get_tasks(params)
    return response, status

@api.route("/api/tasks", methods = ["POST"])
def new_task():
    """Create a new task"""
    if not request.is_json:
        return {"error": "Invalid content type"}, 415
    
    payload = request.json
    response, status = TaskLogic.new_task(payload)
    return response, status

@api.route("/api/tasks/<int:id>", methods = ["PUT"])
def update_task(id):
    """Edit a task"""   
    if not request.is_json:
        return {"error": "Invalid content type"}, 415
    
    payload = request.json
    response, status = TaskLogic.update_task(id, payload)
    return response, status

@api.route("/api/tasks/<int:id>", methods = ["DELETE"])
def delete_task(id):
    """Delete a task"""
    TaskLogic.delete_task(id)
    return "", 204