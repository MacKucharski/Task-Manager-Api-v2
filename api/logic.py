from flask import abort
import sqlalchemy as sa
from sqlalchemy import or_

from api import db
from api.models import User, Task

class TaskLogic:
    
    @staticmethod
    def get_task(id, user):
        """Get task by id"""
        task = db.get_or_404(Task, id)
        #regular user can only request their own task
        if user.role != "admin" and not (user.id != task.created_by_id or user.id != task.assigned_to_id):
            abort(403)
        return task
    
    @staticmethod
    def get_tasks(params, user):
        """Get all tasks according to filters"""
        #regular users can only request their own tasks
        if user.role != "admin":
            condition = [or_(Task.created_by_id == user.id, Task.assigned_to_id == user.id)]
        else:
            condition = [getattr(Task, key) == value for key, value in params.items()]
        query = sa.select(Task).where(*condition)
        print(query)
        tasks = db.session.scalars(query).all()
        return tasks

    @staticmethod
    def new_task(payload, user):
        """Create new task"""
        #regular users cannot assign tasks to other users
        if user.role != "admin":
            payload.pop("assigned_to_it", None)
        payload["created_by_id"] = user.id
        task = Task(**payload)
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def update_task(id, payload, user):
        """Update task according to params"""
        task = db.get_or_404(Task, id)
        if user.role != "admin":
            if user.id != task.created_by_id:
                abort(403)
            else:
                #regular users cannot assign tasks to other users
                payload.pop("assigned_to_id", None)
        for key, value in payload.items():
            setattr(task, key, value)
        db.session.commit()
        return task

    @staticmethod
    def delete_task(id, user):
        """Delete task by id"""
        task = db.get_or_404(Task, id)
        if user.role != "admin" and user.id != task.created_by_id:
            abort(403)
        db.session.delete(task)
        db.session.commit()

class UserLogic:
    
    #all methods require admin rights

    @staticmethod
    def new_user(payload):
        """Create new user"""
        pass

    @staticmethod
    def get_users():
        """Get all users"""
        pass
    
    @staticmethod
    def get_user(id):
        """Get user by id"""
        pass

    @staticmethod
    def delete_user(email):
        """Delete user by email"""
        pass

    @staticmethod
    def upgrade_user(email):
        """Grant user admin rights"""
        pass

    @staticmethod
    def downgrade_user(email):
        """Change user from admin to regular"""
        pass