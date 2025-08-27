from abc import abstractmethod

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.schemas.base_schemas import BaseReadSchema


class DBModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)

    @abstractmethod
    def to_read_schema(self) -> BaseReadSchema:
        raise NotImplemented

    def __str__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"

    def __repr__(self):
        return self.__str__()
