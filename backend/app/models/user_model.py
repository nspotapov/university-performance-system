from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from .abstract_model import AbstractModel


class User(AbstractModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(256), nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
