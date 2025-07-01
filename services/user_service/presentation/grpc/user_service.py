from kink import inject
from datetime import datetime
from utils.validators import jwt_decode
from services.user.config.settings import Settings
from helpers.grpc_module import dict_to_struct
from share_grpc.user.protoc.user_service_pb2 import *
from share_grpc.user.protoc.user_service_pb2_grpc import UserServiceServicer
from services.user.domain.usecase.user import *
from services.user.domain.usecase.role_permission import *
from services.user.domain.usecase.authentication import *
from loguru import logger

@inject
class GetUserInfoServicer(UserServiceServicer):
    def __init__(self, cfg: Settings) -> None:
        super().__init__()
        self.cfg = cfg

    async def _get_users_by_user_ids(self, user_ids):
        get_user_by_id_usecase = UCGetUsersByIds()
        user, failure = await get_user_by_id_usecase.execute(user_ids)

        if failure:
            return None
        return user

    async def _get_role_permission_of_user(self, user_id):
        uc = UCGetRolePermissionOfUser()
        res, failure = await uc.execute(user_id)

        return {} if failure else res

    # get basic info of an user
    async def getBasicUserInfoFromToken(self, request, context):
        token_raw = request.token
        _, _, token = token_raw.partition(" ")
        user = jwt_decode(token, self.cfg.jwt_secret_key)

        # check token exp
        if datetime.strptime(user["exp"], "%Y-%m-%d %H:%M:%S.%f") <= datetime.utcnow():
            logger.info("token expried")
            return BasicUserInfo()
        user = await self._get_users_by_user_ids([user["userId"]])
        if not user:
            logger.info(user)
            return BasicUserInfo()
        user = user[0]

        role_permission = await self._get_role_permission_of_user(str(user.id))

        return BasicUserInfo(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            username=user.username,
            status=user.status,
            phone_number=user.phone_number,
            is_verified=user.is_verified,
            created_at=str(user.created_at.isoformat())
            if isinstance(user.created_at, datetime)
            else user.created_at,
            avatar_url=user.avatar_url,
            role=role_permission["role"] if "role" in role_permission else None,
            permissions=dict_to_struct(role_permission["permissions"])
            if "permissions" in role_permission
            else None,
            profile_status=user.profile_status,
            timezone=user.timezone
        )
