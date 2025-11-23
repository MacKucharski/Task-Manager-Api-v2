# routes related to Task objects

from api import api
from api.logic import TaskLogic
from flask import request, jsonify

@api.route("/api/tasks/<int:id>", methods = ["GET"])
def get_task(id):
    """Retrieve a task by id"""
    task = TaskLogic.get_task(id)
    return jsonify(task.to_dict()), 200

@api.route("/api/tasks", methods = ["GET"])
def get_tasks():
    """Retrieve list of tasks by query params"""
    params = request.args.to_dict()
    tasks = TaskLogic.get_tasks(params)
    return jsonify([task.to_dict() for task in tasks]), 200

@api.route("/api/tasks", methods = ["POST"])
def new_task():
    """Create a new task"""
    if not request.is_json:
        return jsonify({"error": "Invalid content type"}), 415
    
    payload = request.json
    task = TaskLogic.new_task(payload)
    return jsonify(task.to_dict()), 201

@api.route("/api/tasks/<int:id>", methods = ["PUT"])
def update_task(id):
    """Edit a task"""   
    if not request.is_json:
        return jsonify({"error": "Invalid content type"}), 415
    
    payload = request.json
    task = TaskLogic.update_task(id, payload)
    return jsonify(task.to_dict()), 200

@api.route("/api/tasks/<int:id>", methods = ["DELETE"])
def delete_task(id):
    """Delete a task"""
    TaskLogic.delete_task(id)
    return "", 204