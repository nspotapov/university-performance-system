from typing import Generic, TypeVar, Optional, List, Tuple, Any, Dict

from sqlalchemy import select, func, Select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class SQLAlchemyRepository(Generic[ModelType]):
    """Базовый репозиторий для работы с SQLAlchemy"""
    
    model: type[ModelType] = None

    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session

    async def read(self, id: int) -> Optional[ModelType]:
        """Получить запись по ID"""
        query = select(self.model).where(self.model.id == id)
        result = await self.__db_session.execute(query)
        return result.scalar_one_or_none()

    async def find_all(
        self,
        size: int = 50,
        page: int = 1,
        **filters
    ) -> Tuple[List[ModelType], int]:
        """Получить список записей с пагинацией и фильтрами"""
        offset = (page - 1) * size
        
        query = select(self.model)
        count_query = select(func.count()).select_from(self.model)
        
        # Применяем фильтры
        for field, value in filters.items():
            if value is not None:
                query = query.where(getattr(self.model, field) == value)
                count_query = count_query.where(getattr(self.model, field) == value)
        
        # Пагинация
        query = query.offset(offset).limit(size)
        
        results = await self.__db_session.execute(query)
        items = list(results.scalars().all())
        
        count_result = await self.__db_session.execute(count_query)
        total = count_result.scalar()
        
        return items, total

    async def create(self, data: Dict[str, Any]) -> ModelType:
        """Создать запись"""
        instance = self.model(**data)
        self.__db_session.add(instance)
        await self.__db_session.flush()
        await self.__db_session.refresh(instance)
        return instance

    async def update(self, id: int, data: Dict[str, Any]) -> Optional[ModelType]:
        """Обновить запись"""
        instance = await self.read(id)
        if instance is None:
            return None
        
        for field, value in data.items():
            if hasattr(instance, field) and value is not None:
                setattr(instance, field, value)
        
        await self.__db_session.flush()
        await self.__db_session.refresh(instance)
        return instance

    async def delete(self, id: int) -> Optional[ModelType]:
        """Удалить запись"""
        instance = await self.read(id)
        if instance is None:
            return None
        
        await self.__db_session.delete(instance)
        await self.__db_session.flush()
        return instance

    async def find_one(self, **filters) -> Optional[ModelType]:
        """Найти одну запись по фильтрам"""
        query = select(self.model)
        for field, value in filters.items():
            if value is not None:
                query = query.where(getattr(self.model, field) == value)
        
        result = await self.__db_session.execute(query)
        return result.scalar_one_or_none()

    async def find_many(
        self,
        limit: int = 100,
        **filters
    ) -> List[ModelType]:
        """Найти несколько записей по фильтрам"""
        query = select(self.model).limit(limit)
        for field, value in filters.items():
            if value is not None:
                query = query.where(getattr(self.model, field) == value)
        
        result = await self.__db_session.execute(query)
        return list(result.scalars().all())
