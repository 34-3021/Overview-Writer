# 📚 综述写作助手 - Overview Writer

## 🌟 项目简介

综述写作助手是一个基于AI的学术写作辅助工具，帮助用户高效撰写文献综述。系统通过上传论文自动向量化存储，并根据用户需求智能生成论文内容。

### 🛠️ 技术栈
- **前端**: Nuxt3 + NuxtUI
- **后端**: Python + FastAPI
- **数据库**: SQLite
- **向量数据库**: ChromaDB

## 🚀 功能特性
- ✅ 用户认证系统 (JWT)
- 📂 论文上传与向量化存储
- 🔍 智能文献检索
- ✍️ AI辅助论文生成
- 📤 多格式导出 (PDF/Markdown/LaTeX)

## 🛠️ 部署指南

### 1️⃣ 前端部署
```bash
cd frontend
pnpm install
pnpm run dev
```

### 2️⃣ 后端部署
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 3️⃣ 算法服务部署
```bash
cd algo
pip install -r requirements.txt
python main.py
```

## 📂 项目结构

### 前端 (Nuxt3)
```
frontend/
├── app/                 # 前端主目录
│   ├── components/      # 公共组件
│   ├── pages/           # 页面组件
│   ├── store/           # Pinia状态管理
│   └── assets/          # 静态资源
├── nuxt.config.ts       # Nuxt配置
└── package.json         # 前端依赖
```

### 后端 (FastAPI)
```
backend/
├── app/
│   ├── models/          # 数据库模型
│   ├── routers/         # API路由
│   ├── schemas/         # Pydantic模型
│   ├── services/        # 业务逻辑
│   └── main.py          # 主入口
└── requirements.txt     # Python依赖
```

### 算法服务 (FastAPI + Chroma)
```
algorithm/
├── app/
│   ├── models/          # 向量数据库模型
│   ├── routers/         # AI相关API
│   ├── services/        # AI服务逻辑
│   └── main.py          # 主入口
└── requirements.txt     # Python依赖
```

## 🔧 环境配置

### 前端环境变量 (.env)
```env
NUXT_UI_PRO_LICENSE=
HTTP_BASE=http://127.0.0.1:11451
```

## 📌 注意事项

1. 首次运行前需初始化数据库：请运行 backend/app/setup.py。

2. 生产环境建议修改默认密钥和安全配置

3. 确保已安装 Pandoc 以支持 PDF 导出功能

## 📄 许可证
MIT License

---

这个项目将帮助研究人员和学生更高效地撰写学术论文，通过AI技术自动化文献综述的繁琐过程。🎓✨
