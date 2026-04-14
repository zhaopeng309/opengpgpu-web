# OpenGPGPU (观心算力) 后台管理系统增量开发计划

## 📌 计划概述
**目标**: 在现有基础架构（Model + DAO + Service 已完成）之上，完成后台管理系统（Admin Panel）的开发。
**核心功能**: 管理员登录、仪表盘概览、公告管理（CRUD）、Roadmap管理（CRUD）。
**技术栈**: Flask Blueprint (`admin_bp`), Flask-Login (鉴权), Flask-WTF (表单验证), Jinja2。

---

## 📅 增量开发任务拆解

### 阶段一：管理员认证系统 (Auth System)
**目标**: 实现安全的管理员登录与退出机制，保护后台路由。

*   [ ] **任务 1.1**: 编写表单类 (Forms)
    *   创建 `app/forms/admin_form.py`，定义 `LoginForm` (Username, Password, CSRF)。
*   [ ] **任务 1.2**: 登录与退出路由 (Routes)
    *   在 `app/views/admin.py` 中实现 `/admin/login` (GET/POST) 和 `/admin/logout`。
    *   对接 `AdminService.authenticate()` 进行密码比对。
    *   使用 `flask_login.login_user` 和 `logout_user` 管理会话。
*   [ ] **任务 1.3**: 登录页前端渲染 (Templates)
    *   创建 `app/templates/admin/login.html`，保持极简暗黑风格。
    *   处理 Flash 错误消息（如密码错误）。
*   [ ] **测试点**: 尝试访问保护页面应重定向至登录页；输入正确的 `admin`/`admin123` 能够成功登录。

### 阶段二：后台仪表盘 (Dashboard)
**目标**: 提供后台全局概览，统计数据展示。

*   [ ] **任务 2.1**: 后台基础模板 (Admin Base Template)
    *   创建 `app/templates/admin/base.html`，包含后台专属的侧边栏/导航栏（Dashboard, 公告管理, Roadmap管理, 退出登录）。
*   [ ] **任务 2.2**: 仪表盘路由与视图
    *   在 `views/admin.py` 中实现 `/admin/dashboard` (需 `@login_required`)。
    *   调用 Service 层获取统计数据（公告总数、各 Stage 的 Roadmap 数量及进度）。
*   [ ] **任务 2.3**: 仪表盘页面渲染
    *   创建 `app/templates/admin/dashboard.html`，以数据卡片形式展示概览。

### 阶段三：公告管理模块 (Announcement Management)
**目标**: 实现公告的发布、查看、编辑和隐藏（软删除）。

*   [ ] **任务 3.1**: 公告表单
    *   创建 `app/forms/announcement_form.py` (`AnnouncementForm`)。
*   [ ] **任务 3.2**: 公告管理路由
    *   列表页: `/admin/announcements`
    *   新建公告: `/admin/announcement/new`
    *   编辑公告: `/admin/announcement/<id>/edit`
    *   状态切换/删除: `/admin/announcement/<id>/delete`
*   [ ] **任务 3.3**: 公告管理页面
    *   创建 `app/templates/admin/announcements.html` (表格展示)。
    *   创建 `app/templates/admin/announcement_form.html` (复用新建与编辑)。
*   [ ] **测试点**: 在后台发布一条新公告，立刻去前台首页刷新，验证是否实时显示。

### 阶段四：Roadmap 管理模块 (Roadmap Management)
**目标**: 实现 Roadmap 节点的添加、修改、状态变更。

*   [ ] **任务 4.1**: Roadmap 表单
    *   创建 `app/forms/roadmap_form.py` (`RoadmapForm`)。
*   [ ] **任务 4.2**: Roadmap 管理路由
    *   列表页: `/admin/roadmaps`
    *   新建节点: `/admin/roadmap/new`
    *   编辑节点: `/admin/roadmap/<id>/edit`
    *   删除节点: `/admin/roadmap/<id>/delete`
*   [ ] **任务 4.3**: Roadmap 管理页面
    *   创建 `app/templates/admin/roadmaps.html` (按 Stage 分组或直接表格展示)。
    *   创建 `app/templates/admin/roadmap_form.html`。
*   [ ] **测试点**: 在后台将某个 Roadmap 的状态从 "待处理" 改为 "进行中"，前往前台 Roadmap 页面验证颜色和状态是否同步更新。

### 阶段五：UI/UX 调优与交付 (Polishing)
*   [ ] **任务 5.1**: 完善后台响应式布局与极简风格 CSS (`admin.css`)。
*   [ ] **任务 5.2**: 增加操作二次确认提示（如删除操作前的弹窗警告）。
