from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.schemas.user_schemas import UserReadSchema
from .base_model import DBModel


class User(DBModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(256), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)

    def to_read_schema(self) -> UserReadSchema:
        return UserReadSchema(id=self.id, name=self.name, email=self.email, hashed_password=self.hashed_password)
