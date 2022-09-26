import grpc
import json
from kink import inject
from os import environ
from loguru import logger
from core.configs.grpc_server_setting import GrpcServerSettings
from google.protobuf.struct_pb2 import Struct

environ["GRPC_DNS_RESOLVER"] = "native"
environ["GRPC_VERBOSITY"] = "debug"
# environ["GRPC_TRACE"] = "api,cares_resolver,cares_address_sorting,client_channel"


@inject
class GrpcModule:
    """
    Based on the user token, call user info API and inject the user info data to the request
    """

    def __init__(self, grpc_settings: GrpcServerSettings) -> None:
        self.grpc_settings = grpc_settings

    def get_channel(self, service, method,
                    max_attempts=5,
                    initial_backoff="0.1s",
                    max_backoff="10s",
                    backoff_multiplier=2,
                    retryable_status_codes=["UNAVAILABLE"]):
        
        service_name, _ = service.split(".")
        
        # if service_name == "user_service":
        #     self.grpc_settings.GRPC_SERVER_URL="localhost:50051"
       

        
        logger.info(f"Service name: {service_name} --GRPC_server: {self.grpc_settings.GRPC_SERVER_URL} --GRPC_INSECURE: {self.grpc_settings.GRPC_INSECURE}")

        json_config = json.dumps(
            {
                "methodConfig": [
                    {
                        "name": [{
                            "service": service,
                            "method": method
                        }],
                        "retryPolicy": {
                            "maxAttempts": max_attempts,
                            "initialBackoff": initial_backoff,
                            "maxBackoff": max_backoff,
                            "backoffMultiplier": backoff_multiplier,
                            "retryableStatusCodes": retryable_status_codes,
                        },
                    }
                ]
            }
        )

        if self.grpc_settings.GRPC_INSECURE:

            return grpc.aio.insecure_channel(
                self.grpc_settings.GRPC_SERVER_URL,
                options=[("grpc.service_config", json_config)]
            )

        return grpc.aio.secure_channel(
            self.grpc_settings.GRPC_SERVER_URL,
            grpc.ssl_channel_credentials(),
            options=[("grpc.service_config", json_config)]
        )


def dict_to_struct(data: dict):
    struct = Struct()
    struct.update(data)
    return struct