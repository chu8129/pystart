from fastapi import APIRouter, BackgroundTasks
from scene.memory_service import MemoryService
from schema.memory import MemoryResponse

router = APIRouter(prefix="/api", tags=["Memory Monitoring"])

memory_service = MemoryService()


@router.get("/memory", response_model=MemoryResponse, summary="Get Memory Info and Save")
async def get_memory(background_tasks: BackgroundTasks):
    """
    Get current system memory info and save to database

     Returns:
         Detailed memory information including total, used, free memory and usage percentage
    """
    result = await memory_service.get_and_save_memory(background_tasks)
    return result
