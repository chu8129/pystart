from typing import Dict, Any
from enums.memory import StatusLevel
from model.memory import MemoryMetric
from utils.memory import get_memory_usage
from schemas.memory import MemoryInfoSchema
from loguru import logger


class MemoryService:
    """Memory service class"""

    async def get_memory_info(self) -> MemoryInfoSchema:
        """Get current memory information"""
        memory_data = get_memory_usage()
        return MemoryInfoSchema(**memory_data)

    async def save_memory_metric(self, memory_data: Dict[str, Any]) -> MemoryMetric:
        """Save memory metric to database"""
        param = dict(
            metric_type=memory_data["metric_type"],
            usage_percentage=memory_data["percentage"],
            status_level=StatusLevel.from_percentage(memory_data["percentage"]).value,
            status_level_name=StatusLevel.from_percentage(memory_data["percentage"]).name,
            total_memory=memory_data["total"],
            used_memory=memory_data["used"],
            free_memory=memory_data["free"],
            recorded_at=memory_data["recorded_at"],
        )
        logger.debug(f"memory param: {param}")
        metric = await MemoryMetric().aio_create(**param)
        return metric.to_dict()

    async def get_and_save_memory(self) -> Dict[str, Any]:
        """Get and save memory information"""
        memory_data = await self.save_memory_metric(get_memory_usage())
        logger.info(f" Memory metric saved: {memory_data}")
        return {"memory": MemoryInfoSchema(**memory_data), "status": True}
