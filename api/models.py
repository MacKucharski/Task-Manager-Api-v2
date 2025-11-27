from datetime import datetime, timedelta, timezone
import enum
import secrets
import sqlalchemy as sa
from sqlalchemy import orm as so
from typing import Optional

from api import db

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    REGULAR = "regular"

class IDMixin:
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

class User(IDMixin, db.Model):

    __tablename__ = "users"

    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True, nullable=False)
    role: so.Mapped[UserRole] = so.mapped_column(sa.Enum(UserRole, native_enum=False, validate_strings=True, create_constraint=True), nullable=False)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    token: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), index=True, unique=True)
    token_expiration: so.Mapped[Optional[datetime]]

    tasks_created: so.Mapped[list["Task"]] = so.relationship(back_populates="created_by", foreign_keys="Task.created_by_id")
    tasks_assigned: so.Mapped[list["Task"]] = so.relationship(back_populates="assigned_to", foreign_keys="Task.assigned_to_id")

    def __repr__(self) -> str:
        return "<User {}>".format(self.email)
    
    def to_dict(self):
        return {
            "id" : self.id,
            "email" : self.email,
            "role" : self.role,
        }
    
    def get_token(self, expires_in=3600):
        now = datetime.now(timezone.utc)
        if self.token and self.token_expiration.replace(tzinfo=timezone.utc) > now + timedelta(seconds=60): # type: ignore
            return self.token
        self.token = secrets.token_hex(16)
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token
    
    def revoke_token(self):
        self.token_expiration = datetime.now(timezone.utc) - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        query = sa.select(User).where(User.token == token)
        user = db.session.scalar(query)
        if user is None or user.token_expiration.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc): # type: ignore
            return None
        return user

class TaskStatus(str, enum.Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
    CANCELED = "canceled"
    ON_HOLD = "on_hold"

class Task(IDMixin, db.Model):

    __tablename__ = "tasks"

    project: so.Mapped[Optional[str]] = so.mapped_column(sa.String(80), nullable=False)
    name: so.Mapped[str] = so.mapped_column(sa.String(80), nullable=False)
    status: so.Mapped[TaskStatus] = so.mapped_column(sa.Enum(TaskStatus, native_enum=False, validate_strings=True, create_constraint=True), nullable=False)
    created_by_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), nullable=False, index=True)
    assigned_to_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    created_by: so.Mapped[User] = so.relationship(back_populates="tasks_created", foreign_keys=[created_by_id])
    assigned_to: so.Mapped[User] = so.relationship(back_populates="tasks_assigned", foreign_keys=[assigned_to_id])

    def __repr__(self) -> str:
        return "<Task object. Project: {}, name: {}, status: {}, assignee: {}>".format(self.project, self.name, self.status, self.assigned_to_id)
    
    def to_dict(self):
        return {
            "id" : self.id,
            "project" : self.project,
            "name" : self.name,
            "status" : self.status,
            "created by" : self.created_by_id,
            "assigned to" : self.assigned_to_id
        }