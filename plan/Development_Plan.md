# OpenGPGPU 网站开发计划文档 (Development Plan)

## 📌 项目概述
**项目名称**: OpenGPGPU 官方网站
**工作目录**: `/home/designer/public/website/`
**开发策略**: 基于 SQLAlchemy ORM 和 MVC/MVT 严格分层架构，逐步迭代。

---

## 📅 开发任务拆解 (按模块分阶段)

### 阶段一：项目基础架构搭建 (System Setup)
**目标**: 建立标准的 Flask 应用骨架、配置管理和数据库连接。

*   [ ] **任务 1.1**: 初始化 Python 虚拟环境与依赖
    *   创建 `requirements.txt` (包含 Flask, Flask-SQLAlchemy, Flask-Bcrypt, Flask-Login 等)。
    *   配置环境 `.env` 加载与 `config.py` (开发/生产配置切换)。
*   [ ] **任务 1.2**: 实现 Flask 应用工厂模式
    *   创建 `app/__init__.py` 的 `create_app` 函数。
    *   初始化 SQLAlchemy 实例。
*   [ ] **任务 1.3**: 建立 Model 基础层与 DAO 基础层
    *   实现 `app/models/base.py` (`BaseModel`)。
    *   实现 `app/dao/base_dao.py` (`BaseDAO`)。
*   [ ] **测试点**: 确保 `flask run` 能正常启动，数据库初始化脚本能成功创建空表。

### 阶段二：数据模型与访问层开发 (Model & DAO)
**目标**: 完成三大核心实体（Admin, Announcement, Roadmap）的 ORM 映射和数据访问对象。

*   [ ] **任务 2.1**: 管理员模块 (Admin)
    *   编写 `Admin` 模型（包含密码 bcrypt 加密/校验逻辑）。
    *   编写 `AdminDAO`。
*   [ ] **任务 2.2**: 公告模块 (Announcement)
    *   编写 `Announcement` 模型。
    *   编写 `AnnouncementDAO`（含按优先级、活跃状态查询）。
*   [ ] **任务 2.3**: Roadmap 模块
    *   编写 `Roadmap` 模型。
    *   编写 `RoadmapDAO`（含按 Stage 分组、进度统计功能）。
*   [ ] **测试点**: 编写针对三个 DAO 的单元测试/集成测试脚本，确保 CRUD 和特定查询工作正常。

### 阶段三：业务逻辑层开发 (Service Layer)
**目标**: 封装业务逻辑，为视图层提供纯净的 API 接口，并在此层拦截非法数据。

*   [ ] **任务 3.1**: `AdminService`
    *   实现管理员注册（初始化）、身份验证（登录）逻辑。
*   [ ] **任务 3.2**: `AnnouncementService`
    *   实现公告发布（参数长度、类型校验）、修改、软删除、状态统计逻辑。
*   [ ] **任务 3.3**: `RoadmapService`
    *   实现 Roadmap 节点创建（校验 stage 范围和 status）、更新、分组查询、进度计算逻辑。
*   [ ] **测试点**: 编写 `test_services.py` 确保传入非法参数时（如 title 过长，stage 取值错误）正确抛出异常。

### 阶段四：视图控制层与前后端联调 (Views & Templates)
**目标**: 接入前端 HTML，配置 Flask 路由，实现网站功能。

*   [ ] **任务 4.1**: 蓝图注册与静态资源
    *   在应用工厂中注册 `frontend_bp` 和 `admin_bp`。
    *   拷入/创建 CSS、JS、Logo 图片等静态文件到 `static/` 目录。
    *   建立基础模板 `templates/base.html`。
*   [ ] **任务 4.2**: 前台页面开发 (Frontend Views)
    *   `index.html`: 调用 `AnnouncementService.get_latest_announcements()` 渲染公告列表。
    *   `roadmap.html`: 调用 `RoadmapService.get_all_roadmap_grouped()` 渲染开发路线图和状态指示器。
    *   `docs.html` & `community.html`: 静态页面内容渲染。
*   [ ] **任务 4.3**: 后台管理与鉴权 (Admin Views)
    *   配置 `Flask-Login`，实现 `@login_required` 保护。
    *   实现 `/admin/login` 页面及会话管理。
    *   实现 `/admin/dashboard` 页面（用于管理公告和 Roadmap 的增删改查表单页面）。
*   [ ] **测试点**: 启动应用，通过浏览器测试真实账户登录，并测试在后台发布一条公告是否能立即在前台首页展现。

### 阶段五：部署与优化准备 (Deployment & Optimization)
**目标**: 确保系统满足上线要求（安全、性能）。

*   [ ] **任务 5.1**: 安全加固
    *   确保 Session 加密、密码加盐存储配置正确。
    *   检查 Jinja2 模板是否有 XSS 漏洞（默认 autoescape，需确保未被滥用）。
*   [ ] **任务 5.2**: 数据库初始化脚本
    *   编写 `init_db.py` 脚本，用于在服务器一键建表并生成默认 admin 账号和测试数据。
*   [ ] **测试点**: 模拟 Render.com 环境运行 `gunicorn`，检查日志和环境变量加载是否正常。

---

## 🚦 执行规范
1. **测试驱动**: 每一层的开发必须先通过该层的测试，才能进入下一层（如 DAO 测试通过才能写 Service）。
2. **虚拟环境强制**: 所有 Python 依赖必须安装在项目本地的 `venv` 中。
3. **真实验证**: 后台登录开发阶段，禁止 mock 鉴权，必须向数据库插入测试账号并进行真实登录测试。