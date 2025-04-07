# MathHelper 项目部署指南

## 1. 环境准备

### 1.1 基础软件安装
1. 安装 Python 3.8+
   - 访问 [Python官网](https://www.python.org/downloads/) 下载并安装
   - 安装时勾选"Add Python to PATH"

2. 安装 Node.js 16+
   - 访问 [Node.js官网](https://nodejs.org/) 下载并安装

3. 安装 Git
   - 访问 [Git官网](https://git-scm.com/downloads) 下载并安装

### 1.2 OCR环境配置
1. 安装 Tesseract-OCR
   - 访问 [Tesseract-OCR下载页面](https://github.com/UB-Mannheim/tesseract/wiki)
   - 下载并安装最新版本
   - 默认安装路径：`C:\Program Files\Tesseract-OCR`

2. 修改OCR配置
   在 `backend/core/views.py` 中修改 Tesseract 路径：
   ```python
   # 修改为你的实际安装路径
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

### 1.3 API密钥配置
在 `backend/core/views.py` 中配置 Deepseek API：
```python
# 替换为你的API密钥
DEEPSEEK_API_KEY = 'your-api-key-here'
```

## 2. 后端部署

### 2.1 创建虚拟环境
```bash
# 创建项目目录
mkdir MathHelper
cd MathHelper

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2.2 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

### 2.3 数据库配置
```bash
# 创建数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

### 2.4 启动后端服务
```bash
python manage.py runserver
```

## 3. 前端部署

### 3.1 安装依赖
```bash
cd frontend
npm install
```

### 3.2 配置API地址
在 `frontend/src/api/config.ts` 中配置后端API地址：
```typescript
export const API_BASE_URL = 'http://localhost:8000/api'
```

### 3.3 启动开发服务器
```bash
npm run dev
```

## 4. 项目结构说明

### 4.1 后端结构
```
backend/
├── core/                 # 核心应用
│   ├── models.py        # 数据模型
│   ├── views.py         # 视图函数
│   ├── serializers.py   # 序列化器
│   └── urls.py          # URL配置
├── mathhelper/          # 项目配置
├── manage.py           # Django管理脚本
└── requirements.txt    # 依赖列表
```

### 4.2 前端结构
```
frontend/
├── src/
│   ├── api/            # API请求
│   ├── components/     # 组件
│   ├── views/         # 页面
│   ├── stores/        # 状态管理
│   ├── router/        # 路由配置
│   └── types/         # TypeScript类型定义
├── public/            # 静态资源
└── package.json       # 项目配置
```

## 5. 功能测试

### 5.1 用户系统测试
1. 访问 `http://localhost:5173/register` 注册新用户
2. 使用注册的账号登录系统

### 5.2 OCR功能测试
1. 准备一张包含数学题目的图片
2. 在系统中上传图片
3. 检查OCR识别结果和解析

### 5.3 知识图谱测试
1. 使用管理员账号登录后台
2. 添加知识点和关联关系
3. 在前端查看知识图谱展示

## 6. 常见问题解决

### 6.1 OCR识别失败
- 检查Tesseract-OCR是否正确安装
- 确认图片清晰度
- 验证OCR路径配置

### 6.2 API连接失败
- 检查后端服务是否运行
- 验证API地址配置
- 确认网络连接正常

### 6.3 数据库迁移问题
```bash
# 重置数据库
python manage.py migrate core zero
python manage.py makemigrations
python manage.py migrate
```

## 7. 开发建议

### 7.1 代码修改
- 后端API修改：主要在 `core/views.py` 中进行
- 前端页面修改：在 `src/views` 和 `src/components` 中进行
- 样式修改：在 `src/style.css` 中进行

### 7.2 调试技巧
- 使用浏览器开发者工具调试前端
- 使用Django Debug Toolbar调试后端
- 查看后端日志了解详细错误信息

## 8. 注意事项
1. 确保所有依赖版本兼容
2. 定期备份数据库
3. 在生产环境中使用环境变量管理敏感信息
4. 遵循代码规范进行开发
