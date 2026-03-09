import os

# 日志配置 - Logging configuration
LOG_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
    "date_format": os.getenv("LOG_DATE_FORMAT", "%Y-%m-%d %H:%M:%S"),
}
