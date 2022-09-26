import os
from loguru import logger
from  fastapi import FastAPI, Depends
from dotenv import load_dotenv
from .di import init_di
from .configs.setting import cfg
from .presentation.apis.create_user import router as create_user_router

load_dotenv()
api_root_path = os.getenv('API_ROOT_PATH', '')
logger.info(f'API ROOT PATH: {api_root_path}')

app = FastAPI(root_path=api_root_path)

@app.on_event("startup")
async def start_even():
    await init_di()

logger.info(f"App runing!")

app.include_router(create_user_router, prefix=cfg.USER_API_PREFIX)