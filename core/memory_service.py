from typing import Dict, Any

from fastapi import BackgroundTasks
from schema.enums.memory import StatusLevel
from model.memory import MemoryMetric
from utils.memory import get_memory_usage
from schema.memory import MemoryInfoSchema
from loguru import logger


class MemoryService:
    """Memory service class"""

    async def save_memory_metric(self, memory_data: Dict[str, Any], background_tasks: BackgroundTasks) -> MemoryMetric:
        """Save memory metric to database"""
        param = dict(
            metric_type=memory_data["metric_type"],
            usage_percentage=memory_data["percentage"],
            status_level=StatusLevel.from_percentage(memory_data["percentage"]).value,
            status_level_name=StatusLevel.from_percentage(memory_data["percentage"]).name,
            total_memory=memory_data["total"],
            used_memory=memory_data["used"],
            free_memory=memory_data["free"],
            recorded_at=str(memory_data["recorded_at"]),
        )
        logger.debug(f"memory param: {param}")
        background_tasks.add_task(lambda p: print(f"db response: {MemoryMetric().save(p)}"), param)
        return param

    async def get_and_save_memory(self, background_tasks: BackgroundTasks) -> Dict[str, Any]:
        """Get and save memory information"""
        memory_data = await self.save_memory_metric(get_memory_usage(), background_tasks)
        logger.info(f" Memory metric saved: {memory_data}")
        return {"memory": MemoryInfoSchema(**memory_data), "status": True}
