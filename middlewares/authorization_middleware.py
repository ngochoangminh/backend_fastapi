import enum
from fastapi import Request, HTTPException
from typing import Any, List
from core.statics.constant.resources import Resources
from core.response.exception import ( 
    InvalidInputException, 
    ForbiddenException, 
)


class CheckPermissionMiddleware:
    def __init__(self, resource: Resources, actions: List[enum.Enum]):
        self.resource = resource.value
        self.actions = actions

    def __call__(self, request: Request) -> Any:
        user_info = request.state._state.get('user')
        if 'permissions' not in user_info:
            raise InvalidInputException('You do not have any permissions. Please contact admin for more information')
        if self.resource not in user_info['permissions']:
            raise ForbiddenException('You cannot process on this resource.')
        if any(action.value in user_info['permissions'][self.resource] for action in self.actions):
            yield
        else:
            raise ForbiddenException('You cannot process the resource by your permission')
