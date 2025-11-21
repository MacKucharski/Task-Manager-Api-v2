from typing import Optional
import enum

import sqlalchemy as sa
from sqlalchemy import orm as so

from api import db

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    REGULAR = "regular"

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    role: so.Mapped[UserRole] = so.mapped_column(sa.Enum(UserRole), nullable=False)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self) -> str:
        return "<User {}>".format(self.email)

