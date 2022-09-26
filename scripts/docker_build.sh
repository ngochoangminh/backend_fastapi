set -e # STOP ON ERROR

# Variables
SERVICE_NAME=$1
NAME=$(echo my-$SERVICE_NAME | sed -e "s/_/-/g")
VERSION=$2

if [ -z "$SERVICE_NAME" ]
then
      echo "SERVICE NAME MUST NOT BE EMPTY!"
      exit 1
fi
if [ -z "$VERSION" ]
then
      echo "SERVICE VERSION MUST NOT BE EMPTY!"
      exit 1
fi


# echo "{"insecure-registries":["<host>:<port>"]}" > /etc/docker/daemon.json'
# Fetch the .env file
if [ -f ./.env ]; then
    source ./.env
fi

echo "Building ${SERVICE_NAME} Docker image with version ${VERSION}. Push to ${REGISTRY_HOST}/${NAME}"
# Login to docker registry
# ...

# Build production ready docker
docker build -t $NAME:$VERSION -f services/$SERVICE_NAME/deployment/Dockerfile .

# Push to docker registry
docker tag $NAME:$VERSION $REGISTRY_HOST/$NAME:$VERSION
docker push $REGISTRY_HOST/$NAME:$VERSION

# Push as latest
docker tag $REGISTRY_HOST/$NAME:$VERSION $REGISTRY_HOST/$NAME:latest
docker push $REGISTRY_HOST/$NAME:latest
