from typing import Any, Sequence

from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from backend.apps.file_app.models.file_info import FileInfo  # 导入 FileInfo 模型
from backend.apps.file_app.services.crdu import CRUDGen  # 导入 CRUDGen 类


class FileService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_file_infos(self) -> Sequence[Row[Any] | RowMapping | Any]:
        return await CRUDGen.get_all(self.db)

    async def create_file(self, file_info: FileInfo) -> FileInfo:
        return await CRUDGen.create(self.db, file_info)

    async def get_file(self, file_name: str) -> FileInfo:
        file_info = await CRUDGen.get(self.db, file_name)
        if not file_info:
            raise HTTPException(status_code=404, detail="File not found")
        return file_info

    async def update_file(self, file_info: FileInfo) -> FileInfo:
        existing_file = await CRUDGen.get(self.db, file_info.id)
        if not existing_file:
            raise HTTPException(status_code=404, detail="File not found")
        return await CRUDGen.update(self.db, file_info)

    async def delete_file(self, file_id: int) -> None:
        file_info = await CRUDGen.get(self.db, file_id)
        if not file_info:
            raise HTTPException(status_code=404, detail="File not found")
        await CRUDGen.delete(self.db, file_info)