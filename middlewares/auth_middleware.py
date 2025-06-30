from kink import inject, di
from loguru import logger
from typing import Optional
from fastapi import Request, HTTPException, Depends
from common.utils.token.token_helper_util import TokenHelper
from common.response.exception import UnauthorizedException, BaseException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from domain.usecases.users import UCGetRolePermissionOfUserByUserEmail
from settings import Settings
from app.common.statics.constant import CustomRole


class AuthMiddleware(HTTPBearer):

    @inject
    def __init__(
        self,
        cfg: Settings,
        uc_get_role_permission: UCGetRolePermissionOfUserByUserEmail,
        auto_error: bool = True,
        
    ):
        self.token_helper = TokenHelper()
        self.cfg = cfg
        self.uc_get_role_permission = uc_get_role_permission
        super(AuthMiddleware, self).__init__(auto_error=auto_error)

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        decoded_header_request = (
            await self.token_helper.extract_token_from_header_request(
                request=request, token_type=self.token_helper.ACCESS_TOKEN
            )
        )

        if not decoded_header_request:
            raise self._unauthorized_response()
        
        # TODO: add all user data to request state
        email = decoded_header_request.get("sub")
        mode = decoded_header_request.get("mode")
          
        role_permission, fail = await self.uc_get_role_permission.execute(email)
        if fail:
            role_permission = {"role": None, "permissions": None}
            request.state.user = {"email": email, "mode": mode, **role_permission}
            yield
        print(role_permission)
        request.state.user = {"email": email, "mode": mode, "trip_uid": trip_uid, **role_permission}
        yield

        

    @staticmethod
    def _unauthorized_response():
        """
        Generates an unauthorized response.

        Returns:
            HTTPException: HTTPException with 401 status code and error details.
        """

        raise UnauthorizedException("Invalid token or token expired")
