# Python/FastAPI 系统内存监控示例项目

## 项目结构

```
python-examples/
├── api/                    # 接口声明 (API declarations)
├── service/               # 接口逻辑实现 (API logic implementation)
├── utils/                 # 公用libraries (common utilities)
├── provides/              # 公用接口 (common interfaces) - 数据库连接
├── model/                 # 数据库表声明 (database table declarations)
├── schemas/               # pydantic入参声明 (Pydantic input parameter declarations)
├── enums/                 # 枚举数据声明 (enum data declarations)
├── config/                # 各种数据库配置 (database configurations)
├── requirements.txt       # 项目依赖
├── main.py               # 主应用程序入口
└── .env                  # 环境变量配置 (需要创建)
```

## 示例接口：获取系统内存信息

### 功能说明
- **GET /api/memory** - 获取当前系统内存使用情况
- 自动将内存使用数据存储到MySQL数据库
- 使用枚举定义低/中/高三种状态级别
- 基于peewee-async实现异步数据库操作

### 技术特点
- **数据库**: MySQL + peewee-async 异步ORM
- **状态级别**: 低(1)/中(2)/高(3) 三种状态，数据库存储整数
- **内存函数**: utils目录下获取内存使用量
- **数据库连接**: providers模块统一管理，支持重连
- **自动建表**: 程序启动时自动创建数据库表

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置数据库
创建 `.env` 文件：
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=memory_monitor
```

### 3. 运行应用
```bash
python main.py
```

### 4. 测试接口
```bash
# 获取内存信息并自动保存到数据库
curl http://localhost:8000/api/memory

# 查看API文档
# 浏览器访问: http://localhost:8000/docs
```

## 响应示例
```json
{
  "memory": {
    "total": 15.89,
    "used": 8.42,
    "free": 7.47,
    "percentage": 53.0,
    "status_level": 2,
    "status_level_name": "MEDIUM",
    "metric_type": 1,
    "metric_type_name": "MEMORY",
    "recorded_at": "2026-03-09T22:30:00"
  },
  "status": "saved_to_database"
}
```

## 状态级别说明
- **低负载 (1)**: 内存使用率 < 30%
- **中负载 (2)**: 内存使用率 30%-70%
- **高负载 (3)**: 内存使用率 > 70%