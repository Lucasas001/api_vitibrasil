#!/bin/bash

IMAGE_NAME="api_vitibrasil"
CONTAINER_NAME="api_vitibrasil_app"

echo "Build docker imagem..."
docker build -t $IMAGE_NAME .

if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Removing existing container..."
    docker rm -f $CONTAINER_NAME
fi

docker run -it --rm \
    --name $CONTAINER_NAME \
    -p 8000:8000 \
    $IMAGE_NAME
