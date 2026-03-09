from fastapi import APIRouter
from service.memory_service import MemoryService
from schemas.memory import MemoryResponse

router = APIRouter(prefix="/api", tags=["Memory Monitoring"])

memory_service = MemoryService()


@router.get("/memory", response_model=MemoryResponse, summary="Get Memory Info and Save")
async def get_memory():
    """
    获取当前系统内存信息并保存到数据库 - Get current system memory info and save to database

    Returns:
        内存详细信息包括总内存、已使用内存、空闲内存和使用率百分比
        Detailed memory information including total, used, free memory and usage percentage
    """
    result = await memory_service.get_and_save_memory()
    return result
