
from fastapi import APIRouter, Depends

from core.base.base_response import BaseResponse
from ...domain.usecases import CreateUserUsecase
from ..schemas.user_info import *
from ..schemas import *
router = APIRouter()

@router.post(
    '/create-user',
    name='Create User',
    responses={
        400: {"model": BadRequestResponseModel},
        401: {"model": UnauthorizedRequestResponseModel},
        422: {"model": Unprocessable},
        500: {"model": InternalServerErrorModel},
    },
)
async def create_user(
    data: CreateUserRequest,
    usecase: CreateUserUsecase = Depends(lambda: CreateUserUsecase())   
):
    
    user, fail = await usecase.execute(data=data.__dict__)
    if fail:
        return BaseResponse(content=UserInfoResponse(status=fail.code, message=fail.message, data=None))
    return BaseResponse(content=UserInfoResponse(status=200, message="Create User Successfully!", data=user.to_json()))