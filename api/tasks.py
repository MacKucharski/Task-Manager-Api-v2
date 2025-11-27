from flask import jsonify
from flask_pydantic import validate

from api import api
from api.auth import token_auth
from api.logic import TaskLogic
from api.schemas import TaskQuerySchema, TaskCreateSchema, TaskUpdateSchema

@api.route("/api/tasks/<int:id>", methods = ["GET"])
@token_auth.login_required
def get_task(id):
    """Retrieve a task by id"""
    task = TaskLogic.get_task(id)
    return jsonify({"data" : task.to_dict()}), 200

@api.route("/api/tasks", methods = ["GET"])
@token_auth.login_required
@validate()
def get_tasks(query: TaskQuerySchema):
    """Retrieve list of tasks by query params"""
    params = query.model_dump(exclude_none=True)
    tasks = TaskLogic.get_tasks(params)
    return jsonify({"data" : [task.to_dict() for task in tasks]}), 200

@api.route("/api/tasks", methods = ["POST"])
@token_auth.login_required
@validate()
def new_task(body: TaskCreateSchema):
    """Create a new task"""
    user = token_auth.current_user()
    payload = body.model_dump(exclude_none=True)
    task = TaskLogic.new_task(payload, user)
    return jsonify(task.to_dict()), 201

@api.route("/api/tasks/<int:id>", methods = ["PUT"])
@token_auth.login_required
@validate()
def update_task(id, body: TaskUpdateSchema):
    """Edit a task"""
    payload = body.model_dump(exclude_none=True)
    task = TaskLogic.update_task(id, payload)
    return jsonify(task.to_dict()), 200

@api.route("/api/tasks/<int:id>", methods = ["DELETE"])
@token_auth.login_required
def delete_task(id):
    """Delete a task"""
    TaskLogic.delete_task(id)
    return "", 204