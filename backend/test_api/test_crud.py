import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from backend.apps.file_app.services.crdu import CRUDGen

# 定义测试模型
Base = declarative_base()


class TestModel(Base):
    __tablename__ = 'test_model'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


# 创建一个异步引擎和会话
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# 创建异步引擎
engine = create_async_engine(DATABASE_URL, echo=True)

# 创建会话工厂
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# 获取数据库会话的依赖
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # 创建表
    async with AsyncSessionLocal() as session:
        yield session  # 提供会话给测试
        await session.close()  # 测试结束后关闭会话


@pytest.mark.asyncio
async def test_create(db_session):
    model_instance = TestModel(name="Test Name")
    created_instance = await CRUDGen.create(db_session, model_instance)
    assert created_instance.id is not None
    assert created_instance.name == "Test Name"


@pytest.mark.asyncio
async def test_get(db_session):
    model_instance = TestModel(name="Test Name")
    await CRUDGen.create(db_session, model_instance)
    fetched_instance = await CRUDGen.get(db_session, model_instance.id)
    assert fetched_instance is not None
    assert fetched_instance.name == "Test Name"


@pytest.mark.asyncio
async def test_get_all(db_session):
    model_instance1 = TestModel(name="Test Name 1")
    model_instance2 = TestModel(name="Test Name 2")
    await CRUDGen.create(db_session, model_instance1)
    await CRUDGen.create(db_session, model_instance2)
    all_instances = await CRUDGen.get_all(db_session)
    assert len(all_instances) == 2


@pytest.mark.asyncio
async def test_update(db_session):
    model_instance = TestModel(name="Old Name")
    created_instance = await CRUDGen.create(db_session, model_instance)
    created_instance.name = "Updated Name"
    updated_instance = await CRUDGen.update(db_session, created_instance)
    assert updated_instance.name == "Updated Name"


@pytest.mark.asyncio
async def test_delete(db_session):
    model_instance = TestModel(name="Test Name")
    created_instance = await CRUDGen.create(db_session, model_instance)
    await CRUDGen.delete(db_session, created_instance)
    fetched_instance = await CRUDGen.get(db_session, created_instance.id)
    assert fetched_instance is None
