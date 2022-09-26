from pydantic import BaseSettings

class GrpcServerSettings(BaseSettings):
    GRPC_HOST:str ='0.0.0.0'
    GRPC_PORT:int = 50051
    GRPC_SERVER_URL:str
    GRPC_INSECURE: bool=False