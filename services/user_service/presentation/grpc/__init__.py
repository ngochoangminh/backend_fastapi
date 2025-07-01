
from share_grpc.user.protoc.user_service_pb2_grpc import add_UserServiceServicer_to_server
from .user_service import GetUserInfoServicer


def add_service_to_server(server):
    add_UserServiceServicer_to_server(GetUserInfoServicer(), server)