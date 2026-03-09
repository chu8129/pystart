from pydantic import BaseModel, Field


class MemoryInfoSchema(BaseModel):
    """Memory information schema"""

    total_memory: float = Field(..., description="Total memory in GB")
    used_memory: float = Field(..., description="Used memory in GB")
    free_memory: float = Field(..., description="Free memory in GB")
    usage_percentage: float = Field(..., description="Usage percentage")
    status_level: int = Field(..., description="Status level (1=Low, 2=Medium, 3=High)")
    status_level_name: str = Field(..., description="Status level name")
    metric_type: int = Field(..., description="Metric type")
    metric_type_name: str = Field("", description="Metric type name")
    recorded_at: str = Field(..., description="Record time")


class MemoryResponse(BaseModel):
    """Memory response schema"""

    memory: MemoryInfoSchema
    status: str = Field(..., description="Save status")
