"""
环境变量加载器 - Environment Variable Loader
从 MySQL 数据库的 enviroments 表加载环境变量到系统环境变量中
"""

import os
from typing import Dict
from model.enviroment import Environment
from loguru import logger


def load_env_from_db() -> Dict[str, str]:
    """
    从数据库的 enviroments 表加载环境变量

    Returns:
        Dict[str, str]: 加载的环境变量字典
    """
    loaded_envs = {}

    environments = Environment.select()

    for env in environments:
        if env.key and env.value is not None:
            # 更新系统环境变量
            os.environ[env.key] = str(env.value)
            loaded_envs[env.key] = str(env.value)
            logger.debug(f"Loaded environment variable: {env.key}")

    logger.info(f"Successfully loaded {len(loaded_envs)} environment variables from database")

    return loaded_envs
