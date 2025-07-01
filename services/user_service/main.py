import os
import grpc
import uvicorn
from loguru import logger
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .di import init_di
from .config import cfg
from .presentation.api.user.add_refer_code import add_refer_code_router
from .presentation.api.user.get_user_with_refer import get_users_with_refer_router
from .presentation.grpc import add_service_to_server
from .presentation.api.user import *
from .presentation.api.role_permission import *
from .presentation.api.authentication import *
from common.response import BaseException

api_root_path = os.getenv('API_ROOT_PATH', '')
logger.info(f'API ROOT PATH: {api_root_path}')
app = FastAPI(root_path=api_root_path, title="User API")
grpc_server = grpc.aio.server()


@app.on_event("startup")
async def startup_event():
    await init_di()
    add_service_to_server(grpc_server)
    grpc_server.add_insecure_port(f"{cfg.grpc_host}:{cfg.grpc_port}")
    await grpc_server.start()
    logger.info(f"GPRC server is running on {cfg.grpc_host}:{cfg.grpc_port}")


@app.on_event("shutdown")
async def shutdown_event():
    await grpc_server.stop(True)
    await grpc_server.wait_for_termination()

logger.info("Service runinng")


@app.exception_handler(BaseException)
async def base_exception_handler(request: Request, exc: BaseException):
    return JSONResponse(
        status_code=400,
        content={
            "errorCode": exc.error_code,
            "detail": exc.message,
            "data": None
        }
    )

logger.info(f"App runing!")

app.include_router(create_user_router, prefix=cfg.USER_API_PREFIX)