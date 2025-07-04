# python -m grpc_tools.protoc --proto_path=shared_grpc/protos --python_out=shared_grpc --grpc_python_out=shared_grpc shared_grpc/protos/*.proto

PREFIX="protoc/"
SUFFIX=".py"
SERVICE=$1

if [ -z "$SERVICE" ]
then
  echo "\$SERVICE is empty, please provide service to generate grpc."
  exit
fi

cd share_grpc/$SERVICE

[ ! -d "protoc" ] && mkdir "protoc"
if [[ ! -e /protoc/__init__.py ]]; then
  touch protoc/__init__.py
  echo "import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))" > protoc/__init__.py
fi

python -m grpc_tools.protoc --proto_path=protos --python_out=protoc --grpc_python_out=protoc protos/*.proto
for filename in $(find protoc/*_pb2.py)
do
  fixed_filename=${filename#"$PREFIX"}
  fixed_filename=${fixed_filename%"$SUFFIX"}
  grpc_filename=""$PREFIX""$fixed_filename"_grpc"$SUFFIX""
  echo "$(sed "s/import $fixed_filename/from . import $fixed_filename/" $grpc_filename)" > $grpc_filename
done

echo "$SERVICE: generate gRPC protocol python files completed!"