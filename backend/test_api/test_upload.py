import os
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi import Form, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

UPLOAD_DIRECTORY = "/Users/zhangjane/work_space/simple_upload/backend/test_api"  # 确保这个目录存在

app = FastAPI()
router = APIRouter()


@router.post("/upload")
async def upload_files(user: str = Form(...), file: UploadFile = File(...)):
    # 记录用户信息
    print(user)
    # 保存文件到指定目录
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return JSONResponse(content={
                        "message": f"Hello {user}, files uploaded successfully!", "file_paths": file_location})

app.include_router(router)


@pytest.fixture
def client():
    return TestClient(app)


def test_upload_file(client):
    # 创建一个测试文件
    with open("test_file.txt", "w") as f:
        f.write("This is a test file.")

    with open("/Users/zhangjane/work_space/simple_upload/backend/test_api/test_file.txt", "rb") as f:
        response = client.post(
            "/upload",
            data={"user": "test_user"},
            files={"file": ("test_file.txt", f, "text/plain")},
        )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello test_user, files uploaded successfully!",
        "file_paths": os.path.join(UPLOAD_DIRECTORY, "test_file.txt"),
    }

    # 清理测试文件
    os.remove("test_file.txt")
