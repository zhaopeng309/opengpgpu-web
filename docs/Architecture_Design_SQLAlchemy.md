# OpenGPGPU 网站架构设计文档 (SQLAlchemy + 分层架构升级版)

## 📅 文档版本
**版本**: 2.0 (基于极简暴力美学升级)
**核心理念**: 一人公司极简主义 + 标准化企业级后端分层设计

## 🎯 架构升级说明
在保留前端极简、零成本运营的基础上，后端架构全面升级为 **标准 MVC/MVT 分层架构**，引入 **SQLAlchemy ORM**。
这保证了代码的可测试性、可维护性和业务逻辑的解耦，为后续功能扩展打下坚实基础。

## 🏗️ 系统分层架构

```text
┌─────────────────────────────────────────────────────┐
│                 Flask应用层 (Views)                  │
│  • 路由控制 (Routes)                                 │
│  • 模板渲染 (Templates)                              │
│  • 表单处理 (Forms)                                  │
└─────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────┐
│             业务逻辑层 (Service/Action)              │
│  • AnnouncementService - 公告业务逻辑                 │
│  • RoadmapService - Roadmap业务逻辑                  │
│  • AdminService - 管理员业务逻辑                      │
└─────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────┐
│             数据访问层 (DAO/Repository)              │
│  • AnnouncementDAO - 公告数据访问                     │
│  • RoadmapDAO - Roadmap数据访问                      │
│  • AdminDAO - 管理员数据访问                          │
└─────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────┐
│                 数据模型层 (Model)                   │
│  • Announcement - 公告模型                            │
│  • Roadmap - Roadmap模型                             │
│  • Admin - 管理员模型                                 │
└─────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────┐
│            数据库层 (SQLAlchemy + SQLite)            │
│  • SQLite 单文件数据库                                │
│  • SQLAlchemy ORM引擎                                │
└─────────────────────────────────────────────────────┘
```

## 📁 目录结构

```text
opengpgpu-web/
├── app.py                 # Flask应用入口
├── config.py              # 配置文件
├── requirements.txt       # 依赖文件
├── .env                   # 环境变量
├── .gitignore             # Git忽略
├── static/                # 静态资源 (CSS/JS/IMG)
├── templates/             # 模板文件 (HTML)
└── app/                   # 应用核心代码
    ├── __init__.py        # 应用工厂
    ├── models/            # 数据模型层
    │   ├── base.py        # 基础模型 (BaseModel)
    │   ├── announcement.py
    │   ├── roadmap.py
    │   └── admin.py
    ├── dao/               # 数据访问层
    │   ├── base_dao.py    # 基础DAO
    │   ├── announcement_dao.py
    │   ├── roadmap_dao.py
    │   └── admin_dao.py
    ├── services/          # 业务逻辑层
    │   ├── announcement_service.py
    │   ├── roadmap_service.py
    │   └── admin_service.py
    ├── views/             # 视图层 (路由)
    │   ├── frontend.py    # 前台路由 (/, /roadmap, /docs, /community)
    │   └── admin.py       # 后台路由 (/admin/*)
    └── utils/             # 工具函数
```

## 🗃️ 核心分层设计规范

### 1. Model 层 (数据模型)
- 所有模型继承自 `BaseModel` (包含 `id`, `created_at`, `updated_at`, `to_dict`, `save`, `delete`)。
- 使用 `flask_sqlalchemy` 构建实体关系。
- 模型中不包含复杂业务逻辑，仅定义字段和表结构。

### 2. DAO 层 (数据访问)
- 继承自 `BaseDAO`，封装通用的 CRUD 操作 (`get_by_id`, `get_all`, `create`, `update`, `delete`, `filter_by`, `count`)。
- 隔离 ORM 细节，上层无需直接操作 `db.session`。

### 3. Service 层 (业务逻辑)
- 处理业务规则、输入验证、异常抛出。
- 组装 DAO 提供的方法，向 View 层暴露纯粹的业务接口。
- 例如：`create_roadmap_item` 需验证 stage 范围、status 合法性。

### 4. View 层 (视图路由)
- 使用 Flask Blueprints (`frontend_bp`, `admin_bp`) 组织路由。
- 接收 HTTP 请求，解析参数，调用 Service 层，渲染 Jinja2 模板并返回 HTTP 响应。
- 捕获 Service 层抛出的异常，转化为 Flash 消息或 HTTP 错误码返回。

## 🎨 前端与部署策略
- 保持极简暴力美学：纯 HTML/CSS/JS，无繁重框架。
- 统一部署在 Render.com 免费套餐，配合 Cloudflare CDN。
