import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from backend.apps.file_app.models import FileInfo
from backend.common.path_conf import UPLOAD_DIRECTORY
from backend.common.response.response_code import StandardResponseCode
from backend.databases.async_db_mysql import get_db
from backend.utils.serializers import select_list_serialize, select_as_dict
from backend.utils.tools import md5_file, get_url_suffix, clean_file_name

router = APIRouter()


def standard_response(code: int, message: str, result: dict | list = None):
    return JSONResponse(content={"code": code, "message": message, "result": result})


@router.get("/all_files")
async def get_all_file_list(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        total_count_result = await db.execute(
            select(func.count()).select_from(FileInfo).where(FileInfo.is_deleted == 0))
        total_count = total_count_result.scalar()
        result = await db.execute(select(FileInfo).where(FileInfo.is_deleted == 0).offset(skip).limit(limit))
        files = result.scalars().all()
        serialize_files_obj = await select_list_serialize(files)
        return JSONResponse(
            content={
                "code": StandardResponseCode.HTTP_200,
                "message": "Files retrieved successfully",
                "result": serialize_files_obj,
                "total_count": total_count
            })
    except Exception as e:
        raise HTTPException(status_code=StandardResponseCode.HTTP_500, detail=f"An error occurred: {str(e)}")


@router.get("/search/{file_name}")
async def search_file(file_name: str, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(FileInfo).where(FileInfo.file_name.like(f"{file_name}%"), FileInfo.is_deleted == 0))
        file_info_list = result.scalars().all()
        if not file_info_list:
            raise HTTPException(status_code=404, detail="File not found")
        serialized_files = await select_list_serialize(file_info_list)
        return standard_response(StandardResponseCode.HTTP_200, "Files found", serialized_files)
    except Exception as e:
        raise HTTPException(status_code=StandardResponseCode.HTTP_500, detail=f"An error occurred: {str(e)}")


@router.get("/file/{file_name}")
async def get_file(file_name: str, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(FileInfo).where(FileInfo.file_name == file_name, FileInfo.is_deleted == 0))
        file_info = result.scalar_one_or_none()
        if not file_info:
            raise HTTPException(status_code=404, detail="File not found")
        serialize_file_obj = await select_as_dict(file_info)
        return standard_response(StandardResponseCode.HTTP_200, "File retrieved successfully", serialize_file_obj)
    except Exception as e:
        raise HTTPException(status_code=StandardResponseCode.HTTP_500, detail=f"An error occurred: {str(e)}")


@router.delete("/delete/{pk_id}")
async def delete_file(pk_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(FileInfo).where(FileInfo.id == pk_id, FileInfo.is_deleted == 0))
        file_info = result.scalar_one_or_none()
        if file_info is None:
            raise HTTPException(status_code=404, detail="File not found or already deleted")

        file_info.is_deleted = 1
        await db.commit()
        return standard_response(StandardResponseCode.HTTP_200, "File deleted successfully")
    except Exception as e:
        raise HTTPException(status_code=StandardResponseCode.HTTP_500, detail=f"An error occurred: {str(e)}")


@router.get("/download/{file_name}")
async def download_files(file_name: str):
    file_name = clean_file_name(file_name)
    file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=StandardResponseCode.HTTP_404, detail="File not found")

    return FileResponse(file_path, media_type='application/octet-stream', filename=file_name)


@router.post("/upload")
async def upload_files(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    try:
        file_type = get_url_suffix(file.filename)
        file_name = clean_file_name(file.filename)
        file_location = os.path.join(UPLOAD_DIRECTORY, file_name)
        if not os.path.exists(file_location):
            with open(file_location, "wb") as f:
                file_bytes = await file.read()
                f.write(file_bytes)
                uuid = md5_file(file_bytes)

            file_size = os.path.getsize(file_location)
            save_json_data = {"uuid": uuid, "file_name": file_name, "file_type": file_type, "file_size": file_size}

            file_info = FileInfo(**save_json_data)
            db.add(file_info)
            await db.commit()
            await db.refresh(file_info)
            return standard_response(StandardResponseCode.HTTP_200, "File uploaded successfully", save_json_data)
        else:
            return standard_response(StandardResponseCode.HTTP_200, "Duplicate uploads", {"file_name": file_name})
    except FileNotFoundError:
        raise HTTPException(status_code=StandardResponseCode.HTTP_400, detail="Upload directory not found.")
    except Exception as e:
        raise HTTPException(status_code=StandardResponseCode.HTTP_500, detail=f"An error occurred: {str(e)}")
