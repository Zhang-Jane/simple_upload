from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi_pagination import add_pagination

from backend.apps.router import route
from backend.common.exceptions.exception_handler import register_exception
from backend.common.log import set_customize_logfile, setup_logging
from backend.common.conf import settings
from backend.common.path_conf import STATIC_DIR
from backend.databases.async_db_mysql import create_table
from backend.databases.async_db_redis import redis_client
from backend.utils.health_check import ensure_unique_route_names, http_limit_callback
from backend.utils.openapi import simplify_operation_ids
from backend.utils.serializers import MsgSpecJSONResponse


@asynccontextmanager
async def register_init(app: FastAPI):
    """
    启动初始化

    :return:
    """
    # # 创建数据库表
    await create_table()
    # 连接 redis
    await redis_client.open()
    # 初始化 limiter
    await FastAPILimiter.init(redis_client, prefix=settings.LIMITER_REDIS_PREFIX, http_callback=http_limit_callback)

    yield

    # # 关闭 redis 连接
    await redis_client.close()
    # 关闭 limiter
    await FastAPILimiter.close()


def register_app():
    env = settings.ENVIRONMENT
    # 初始化application
    if env != 'pro':
        app = FastAPI(
            title=settings.TITLE,
            version=settings.VERSION,
            description=settings.DESCRIPTION,
            docs_url=settings.DOCS_URL,
            redoc_url=settings.REDOCS_URL,
            openapi_url=settings.OPENAPI_URL,
            default_response_class=MsgSpecJSONResponse,
            lifespan=register_init,
        )
    else:
        app = FastAPI(
            title=settings.TITLE,
            version=settings.VERSION,
            description=settings.DESCRIPTION,
            docs_url=None,
            redoc_url=None,
            openapi_url=settings.OPENAPI_URL,
            default_response_class=MsgSpecJSONResponse,
            lifespan=register_init,
        )

    # 日志
    register_logger()

    # 静态文件
    register_static_file(app)

    # 中间件
    # register_middleware(app)

    # 路由
    register_router(app)

    # 全局异常处理
    register_exception(app)

    return app


def register_logger() -> None:
    """
    系统日志

    :return:
    """
    setup_logging()
    set_customize_logfile()


def register_static_file(app: FastAPI):
    """
    静态文件交互开发模式, 生产使用 nginx 静态资源服务

    :param app:
    :return:
    """
    if settings.STATIC_FILES:
        import os

        from fastapi.staticfiles import StaticFiles

        if not os.path.exists(STATIC_DIR):
            os.mkdir(STATIC_DIR)
        app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')


def register_middleware(app: FastAPI):
    """
    中间件，执行顺序从下往上

    :param app:
    :return:
    """
    # Access log
    if settings.MIDDLEWARE_ACCESS:
        from backend.middleware.access_middleware import AccessMiddleware
        app.add_middleware(AccessMiddleware)
    # CORS: Always at the end
    if settings.MIDDLEWARE_CORS:
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )


def register_router(app: FastAPI):
    """
    路由

    :param app: FastAPI
    :return:
    """

    # API
    app.include_router(route)

    # Extra
    ensure_unique_route_names(app)
    simplify_operation_ids(app)


def register_page(app: FastAPI):
    """
    分页查询

    :param app:
    :return:
    """
    add_pagination(app)
