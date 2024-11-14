## 文件上传demo

### 前端目录
```html
├── frontend
│   ├── src
│   │   ├── components
│   │   │   └── FileUpload.vue  # 文件上传组件
│   │   ├── views
│   │   │   └── UploadView.vue   # 上传视图
│   │   ├── router
│   │   │   └── index.js          # 路由配置
│   │   ├── App.vue                # 主应用组件
│   │   └── main.js                # 入口文件
│   └── public
│       └── index.html             # HTML 模板
└── package.json                   # 项目配置
```
### 后端目录结构
```html
├── backend
    ├── __init__.py
    ├── apps（含不同的应用模块）
    ├── databases（数据库连接）
    ├── db_sql（一些sql语句）
    ├── middleware（全局中间件）
    ├── models（orm的模型定于）
    ├── scripts（脚本）
    ├── test_api（测试api）
    └── utils
├── README.md
├── alembic.ini（数据库迁移脚本配置）
├── Dockerfile
├── Makefile
├── docker-compose.yml
├── logging.conf（日志配置）
├── poetry.lock
└── pyproject.toml
```

目录架构参考：

| 工作流程 | Django            | Java           | fastapi_best_architecture |
| -------- | ----------------- | -------------- | ------------------------- |
| 视图     | views             | controller     | api                       |
| 数据传输 | serializers       | dto            | schema                    |
| 业务逻辑 | models (或 views) | service + impl | service                   |
| 数据访问 | models            | dao / mapper   | crud                      |
| 模型     | models            | model / entity | model                     |


**视图 (View):**

* Java: 通常使用控制器（Controller）来处理HTTP请求和响应，负责将请求映射到相应的业务逻辑。
* FastAPI: 使用API路由（api）来定义端点，处理请求并返回响应。
* Django: 使用视图（views）来处理请求，通常是函数或类视图，负责业务逻辑和返回响应。

**数据传输 (Data Transfer):**

* Java: 使用数据传输对象（DTO）来封装数据，通常用于在不同层之间传递数据。
* FastAPI: 使用模式（schema），通常是Pydantic模型，用于验证和序列化请求和响应数据。
* Django: 使用序列化器（serializers），用于将复杂数据类型（如查询集）转换为Python数据类型，并进行验证。

**业务逻辑 (Business Logic):**

* Java: 通常在服务层（service）和实现类（impl）中处理业务逻辑，分离接口和实现。
* FastAPI: 业务逻辑通常在服务层（service）中实现，保持路由和业务逻辑的分离。
* Django: 业务逻辑通常在模型（models）中实现，或者在视图（views）中直接处理。

**数据访问 (Data Access):**

* Java: 使用数据访问对象（DAO）或映射器（mapper）来处理数据库操作，通常与ORM结合使用。
* FastAPI: 使用CRUD操作来处理数据库交互，通常结合ORM（如SQLAlchemy）使用。
* Django: 使用模型（models）直接与数据库交互，Django的ORM提供了强大的查询功能。

**模型 (Model):**
* Java: 使用模型（model）或实体（entity）来定义数据结构，通常与数据库表对应。
* FastAPI: 使用模型（model）来定义数据结构，通常是Pydantic模型或SQLAlchemy模型。
* Django: 使用模型（models）来定义数据结构，Django的ORM会根据模型自动创建数据库表。