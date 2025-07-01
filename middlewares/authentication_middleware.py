
from kink import inject
from loguru import logger
from fastapi import HTTPException, Request
from common.response import *
from helpers import GrpcModule
from share_grpc.user.protoc.user_service_pb2 import BasicUserInfoFromTokenRequest, BasicUserInfo
from share_grpc.user.protoc.user_service_pb2_grpc import UserServiceStub
from google.protobuf.json_format import MessageToDict


class AuthMiddleware(HTTPBearer):

    @inject
   
    def __init__(self, grpc_module: GrpcModule) -> None:
        self.grpc_module = grpc_module

    async def __call__(self, request: Request):
        token_raw = request.headers.get('Authorization')
        request.state.user = await self.extract_user_from_token(token_raw)
        yield

    async def extract_user_from_token(self, token_raw: str):
        if token_raw is not None:
            async with self.grpc_module.get_channel("user_service.UserServices", 'getBasicUserInfoFromToken') as channel:
                stub = UserServiceStub(channel)
                response: BasicUserInfo = await stub.getBasicUserInfoFromToken(BasicUserInfoFromTokenRequest(token=token_raw))
            logger.debug(MessageToDict(response))
            if response.status.lower() == "blocked":
                raise HTTPException(status_code=401)
            return MessageToDict(response)
        else:
            return None
