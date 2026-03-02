import uuid
from abc import abstractmethod

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.schemas.base_schemas import BaseReadSchema


class DBModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(256),
        primary_key=True,
        index=True,
        insert_default=str(uuid.uuid4())
    )

    @abstractmethod
    def to_read_schema(self) -> BaseReadSchema:
        raise NotImplemented

    def __str__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"

    def __repr__(self):
        return self.__str__()
