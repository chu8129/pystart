import psutil
from datetime import datetime
from typing import Dict, Any
from enums.memory import MetricType


def get_memory_usage() -> Dict[str, Any]:
    """
    获取内存使用量 - Get memory usage

    Returns:
        Dict containing memory information:
        - total: Total memory in GB
        - used: Used memory in GB
        - free: Free memory in GB
        - percentage: Usage percentage
    """
    # 获取内存信息 - Get memory information
    memory = psutil.virtual_memory()

    # 转换为GB单位 - Convert to GB units
    total_gb = round(memory.total / (1024**3), 2)
    used_gb = round(memory.used / (1024**3), 2)
    free_gb = round(memory.available / (1024**3), 2)
    percentage = round(memory.percent, 2)

    return {
        "total": total_gb,
        "used": used_gb,
        "free": free_gb,
        "percentage": percentage,
        "metric_type": MetricType.MEMORY.value,
        "metric_type_name": MetricType.MEMORY.name,
        "recorded_at": datetime.now(),
    }
