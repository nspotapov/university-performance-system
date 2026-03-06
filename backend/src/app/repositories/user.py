from app.models import User
from app.repositories.sqlalchemy import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User
