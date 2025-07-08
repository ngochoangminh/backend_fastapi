
import pytest
import pytest_asyncio
import json

from kink import di
from loguru import logger

from services.user.config import cfg
from fastapi.testclient import TestClient
from fastapi import Response
from helpers import GrpcModule
from utils.ext.auth_providers import OauthClient
from helpers import RedisHelper
from services.user.data.repository_impl import UserServiceRepoImp
from services.user.domain.repository import UserServiceRepository
from services.user.main import app
from services.user.entities import User
from services.user.domain.usecase.authentication import UCLoginEmailOrUsernamePassword

from unittest.mock import MagicMock, AsyncMock


@pytest.mark.asyncio
async def test_login_success(app_client):
    # ====== Arrange
    # Create mock data

    # client = TestClient(app)

    mock_input_data = {
        'identinity': 'hoanq@arrowhitech.net',
        'password': 'Ohio@2023'
    }
    mock_token = "Bearer lakdsjfklasdfklajsdlfkjaslk"
    mock_result_user = {
        "id": "2086c136-c13d-4105-b515-d9cd68248e39",
        "first_name": 'Viktor',
        "last_name": 'Vu',
        "email": 'hoanq@arrowhitech.net',
        "username": 'viktor_vu',
        "is_created": True,
        "is_verified": False,
        "status": "ACTIVE",
        "is_deleted": False,
        "flag_must_change_password": False
    }

    mock_usecase = UCLoginEmailOrUsernamePassword()
    di[UCLoginEmailOrUsernamePassword] = mock_usecase
    mock_usecase.execute = AsyncMock(return_value=(mock_result_user, mock_token, None))

    # ====== Act
    response: Response = app_client.post(url='/login', json=mock_input_data)
    print('res', response)

    # ====== Assert
    # assert status code and response
    assert response.status_code == 200
    assert response.headers.get('authorization') == mock_token

    # mock_usecase.execute.assert_awaited_once_with(
    #     identinity=mock_input_data["identinity"], 
    #     password=mock_input_data["password"]
    #     )
