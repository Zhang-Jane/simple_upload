import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.common.log import log
from backend.common.model import MappedBase
from backend.common.conf import settings


def create_engine_and_session(url: str):
    try:
        # 创建数据库引擎
        engine = create_engine(url, echo=settings.MYSQL_ECHO, future=True)
        log.success('数据库连接成功')
    except Exception as e:
        log.error('❌ 数据库链接失败 {}', e)
        sys.exit()
    else:
        db_session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
        return engine, db_session


SQLALCHEMY_DATABASE_URL = (f'mysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:'
                           f'{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}?charset={settings.MYSQL_CHARSET}')

sync_engine, sync_db_session = create_engine_and_session(SQLALCHEMY_DATABASE_URL)


def create_table():
    """创建数据库表"""
    with sync_engine.begin() as conn:
        conn.run_sync(MappedBase.metadata.create_all)
