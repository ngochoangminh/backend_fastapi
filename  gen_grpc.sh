python -m grpc_tools.protoc --proto_path=shared_grpc/protos --python_out=shared_grpc --grpc_python_out=shared_grpc shared_grpc/protos/*.proto