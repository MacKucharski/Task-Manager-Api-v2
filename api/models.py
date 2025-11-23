from typing import Optional
import enum

import sqlalchemy as sa
from sqlalchemy import orm as so

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
            "status" : self.status,
            "created by" : self.created_by_id,
            "assigned to" : self.assigned_to_id
        }