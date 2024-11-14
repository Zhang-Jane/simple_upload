from typing import TypeVar, Generic, Any, Sequence

from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class CRUDGen(Generic[ModelType]):

    @staticmethod
    async def create(db: AsyncSession, model: ModelType) -> ModelType:
        db.add(model)
        await db.commit()
        await db.refresh(model)
        return model

    @staticmethod
    async def get(db: AsyncSession, file_name: str) -> ModelType:
        return await db.get(ModelType, file_name)

    @staticmethod
    async def get_all(db: AsyncSession) -> Sequence[Row[Any] | RowMapping | Any]:
        result = await db.execute(select(ModelType))
        return result.scalars().all()

    @staticmethod
    async def update(db: AsyncSession, model: ModelType) -> ModelType:
        await db.commit()
        await db.refresh(model)
        return model

    @staticmethod
    async def delete(db: AsyncSession, model: ModelType) -> None:
        await db.delete(model)
        await db.commit()
