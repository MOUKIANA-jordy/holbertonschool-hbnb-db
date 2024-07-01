"""
User related functionality
"""

import datetime
from src.models.base import Base
from sqlalchemy.orm import relationship
import uuid
from src.persistence import repo
from src.models.base import BaseModel
from sqlalchemy import Column, String, Boolean, DateTime
from flask_bcrypt import Bcrypt

class User(Base):
    """User representation"""

    __tablename__ = 'user'

    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    def __init__(self, email: str, first_name: str, last_name: str, **kw):
        """Dummy init"""
        super().__init__(**kw)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<User {self.id} ({self.email})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
             "is_admin": self.is_admin,
        }

    @staticmethod
    def create(user: dict) -> "User":
        """Create a new user"""

        users: list["User"] = User.get_all()

        for u in users:
            if u.email == user["email"]:
                raise ValueError("User already exists")

        new_user = User(**user)

        repo.save(new_user)

        return new_user

    @staticmethod
    def update(user_id: str, data: dict) -> "User | None":
        """Update an existing user"""

        user: User | None = User.get(user_id)

        if not user:
            return None

        if "email" in data:
            user.email = data["email"]
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]
        if "password" in data:
            user.password = data["password"]
        if "is_admin" in data:
            user.is_admin = data["is_admin"]

        repo.update(user)

        return user
    
    @staticmethod
    def set_password(self, password):
         self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
         return bcrypt.check_password_hash(self.password_hash, password)
