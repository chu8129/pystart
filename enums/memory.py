from enum import IntEnum


class StatusLevel(IntEnum):
    """Status level enumeration"""

    LOW = 1  # 低 - Low
    MEDIUM = 2  # 中 - Medium
    HIGH = 3  # 高 - High

    @classmethod
    def from_percentage(cls, percentage: float) -> "StatusLevel":
        """Get status level from percentage"""
        if percentage < 30:
            return cls.LOW
        elif percentage < 70:
            return cls.MEDIUM
        else:
            return cls.HIGH


class MetricType(IntEnum):
    """Metric type enumeration"""

    MEMORY = 1  # 内存 - Memory
    CPU = 2  # CPU - CPU
