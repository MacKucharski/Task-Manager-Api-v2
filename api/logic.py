# business logic operating on User and Task objects

MOCK_TASKS_LIST = {
    "tasks": [
    {"id": "1", "description": "Task 1", "status": "in progress"},
    {"id": "2", "description": "Task 2", "status": "completed"},
    {"id": "3", "description": "Task 3", "status": "new"},
    {"id": "4", "description": "Task 4", "status": "new"},
    {"id": "5", "description": "Task 5", "status": "in progress"},
    {"id": "6", "description": "Task 6", "status": "in progress"},
    {"id": "7", "description": "Task 7", "status": "canceled"}
    ]}


class TaskLogic:

    @staticmethod
    def new_task(payload):
        return "Not implemented", 200
    
    @staticmethod
    def get_task(id):
        return [task for task in MOCK_TASKS_LIST["tasks"] if task["id"] == id], 200
    
    @staticmethod
    def get_tasks(params):
        # filtering to be implemented
        return MOCK_TASKS_LIST, 200

    @staticmethod
    def update_task(id, payload):
        return "Not implemented", 200

    @staticmethod
    def delete_task(id):
        return "Not implemented", 200


class UserLogic:

    @staticmethod
    def get_users():
        pass
    
    @staticmethod
    def get_user(id):
        pass