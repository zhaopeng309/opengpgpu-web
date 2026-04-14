# OpenGPGPU Project Website

这是 **OpenGPGPU** 项目的官方网站。该平台主要用于向用户实时展示项目的进展情况，提供官方公告、开发路线图(Roadmap)、文档指引及社区交流资源。

## ✨ 核心功能

- **项目公告**：发布 OpenGPGPU 项目的最新动态与版本发布信息。
- **开发路线图 (Roadmap)**：展示项目过往已完成目标、当前正在进行的工作，以及未来的版本规划。
- **项目文档**：提供技术架构文档、用户使用指南等入口。
- **社区建设**：帮助用户快速加入 OpenGPGPU 社区进行交流讨论。
- **后台管理**：支持管理员通过后台发布和管理公告及路线图数据。

## 🛠️ 技术栈

本项目基于 Python Web 生态构建：
- **后端框架**：Flask 3.x
- **数据库 ORM**：Flask-SQLAlchemy (SQLAlchemy 2.x)
- **数据库**：SQLite (本地/默认)
- **表单验证**：Flask-WTF
- **认证管理**：Flask-Login, Flask-Bcrypt
- **部署**：Gunicorn, 支持 Render 等 PaaS 平台部署

## 📂 项目结构

```text
.
├── app/                  # Flask 核心应用目录
│   ├── dao/              # 数据访问层 (Data Access Object)
│   ├── forms/            # Web 表单及验证逻辑
│   ├── models/           # 数据库模型
│   ├── services/         # 业务逻辑层
│   ├── static/           # 静态资源 (CSS, JS, 图像)
│   ├── templates/        # Jinja2 网页模板 (前台与 Admin 后台)
│   ├── views/            # 路由控制器 (前台展示与后台管理)
│   └── extensions.py     # Flask 扩展初始化
├── docs/                 # 项目文档与技术架构说明
├── plan/                 # 项目开发计划文件
├── tests/                # 基于 pytest 的自动化测试用例
├── instance/             # 存放本地 SQLite 数据库等实例文件
├── config.py             # 项目不同环境的配置项 (开发/测试/生产)
├── init_db.py            # 数据库初始化脚本（含初始数据与默认管理员）
├── requirements.txt      # Python 依赖包列表
├── render.yaml           # Render 平台云端部署配置文件
└── wsgi.py               # WSGI 应用部署与启动入口
```

## 🚀 本地开发与运行

### 1. 环境准备

确保您的系统中已安装 Python 3.8+。强烈建议在虚拟环境中运行此项目：

```bash
# 进入项目目录
cd website

# 创建并激活虚拟环境
python3 -m venv venv

# Linux/macOS
source venv/bin/activate  
# Windows
# venv\Scripts\activate   
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 初始化数据库

运行初始化脚本，它会创建数据库表并自动写入初始演示数据（包含默认的管理员账号）：

```bash
python init_db.py
```

*系统默认管理员账号:*
- 用户名: `admin`
- 密码: `admin123`

### 4. 启动服务

使用本地开发服务器启动网站：

```bash
python wsgi.py
```

终端将提示服务已启动，网站默认运行在 `http://127.0.0.1:5000/`。

## 🛡️ 后台管理

在浏览器访问 `http://127.0.0.1:5000/admin` 进入后台管理系统。
使用初始化的管理员账号登录后，即可执行以下操作：
- **管理员控制台**：数据概览。
- **公告管理**：创建、编辑、删除以及置顶公告。
- **路线图管理**：更新开发阶段任务，调整路线图状态（Pending/In Progress/Completed）。

## 🧪 运行测试

本项目包含单元测试，用于确保 Service/DAO 层的业务逻辑稳定。请在虚拟环境激活状态下执行：

```bash
pytest
```

## ☁️ 部署

项目包含 `render.yaml`，可通过 [Render](https://render.com) 平台实现零配置的自动化持续部署，生产服务入口配置为 `gunicorn wsgi:app`。

## 📄 许可证

本项目遵循 [LICENSE](./LICENSE) 文件中指定的开源协议。
