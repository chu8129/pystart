import os
from dotenv import load_dotenv

# 加载环境变量 - Load environment variables
load_dotenv()

# 数据库配置 - Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "memory_monitor"),
    "charset": "utf8mb4",
}

# FastAPI配置 - FastAPI configuration
API_CONFIG = {
    "title": "qw",
    "version": "0.01",
    "description": "",
}
