import datetime
from peewee import AutoField, IntegerField, FloatField, DateTimeField

from schema.enums.memory import MetricType, StatusLevel
from . import BaseModel


class MemoryMetric(BaseModel):
    """Memory metric model"""

    id = AutoField(primary_key=True)
    metric_type = IntegerField(default=MetricType.MEMORY.value)
    usage_percentage = FloatField()
    status_level = IntegerField()
    total_memory = FloatField()
    used_memory = FloatField()
    free_memory = FloatField()
    recorded_at = DateTimeField(default=datetime.datetime.now)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "memory_metrics"

    def to_dict(self):
        """Convert to dictionary"""

        # 获取状态级别 - Get status level
        status_level = StatusLevel.from_percentage(self.usage_percentage)
        return {
            "id": self.id,
            "metric_type": self.metric_type,
            "usage_percentage": self.usage_percentage,
            "status_level": status_level.value,
            "status_level_name": status_level.name,
            "total_memory": self.total_memory,
            "used_memory": self.used_memory,
            "free_memory": self.free_memory,
            "recorded_at": self.recorded_at.isoformat() if self.recorded_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
