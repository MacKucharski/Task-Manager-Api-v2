import sqlalchemy as sa

from api import db
from api.models import User, Task

class TaskLogic:

    @staticmethod
    def new_task(payload, user):
        """Create new task"""
        payload["created_by_id"] = user.id
        task = Task(**payload)
        db.session.add(task)
        db.session.commit()
        return task
    
    @staticmethod
    def get_task(id):
        """Get task by id"""
        return db.get_or_404(Task, id)
    
    @staticmethod
    def get_tasks(params):
        """Get all tasks according to filters"""
        condition = [getattr(Task, key) == value for key, value in params.items()]
        query = sa.select(Task).where(*condition)
        tasks = db.session.scalars(query).all()
        return tasks

    @staticmethod
    def update_task(id, payload):
        """Update task according to params"""
        task = db.get_or_404(Task, id)
        for key, value in payload.items():
            setattr(task, key, value)
        db.session.commit()
        return task

    @staticmethod
    def delete_task(id):
        """Delete task by id"""
        task = db.get_or_404(Task, id)
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