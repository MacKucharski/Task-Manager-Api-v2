import sqlalchemy as sa
from sqlalchemy import orm as so

from api import api, db
from api.models import User, Task
from api.logic import TaskLogic as tl

@api.shell_context_processor
def make_shell_context():
    return {"sa":sa, "so":so, "db":db, "User":User, "Task":Task, "tl":tl}