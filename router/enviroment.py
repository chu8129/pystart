"""
环境变量路由 - Environment Variable Router
提供手动刷新环境变量的接口
"""

import logging
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

from utils.env_loader import load_env_from_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/env", tags=["env variables"])


class EnvRefreshResponse(BaseModel):
    """环境变量刷新响应"""

    message: str
    count: int
    variables: Dict[str, str]


@router.get("/refresh", response_model=Dict[str, str])
async def list_environment_variables():
    """
    列出当前已加载的数据库环境变量

    注意：这只是从数据库加载的环境变量，不是系统全部环境变量
    """
    return load_env_from_db()
