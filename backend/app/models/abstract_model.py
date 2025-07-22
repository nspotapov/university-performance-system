from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class AbstractModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)

    def __str__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"

    def __repr__(self):
        return self.__str__()
