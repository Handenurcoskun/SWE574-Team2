#!/bin/bash

image_name=$1

# Stop existing container
docker rm $(docker ps -aq) -f || true

# Pull latest Docker image
docker pull $image_name

# Run the latest container
docker run -d --name your_container_name --restart always -p 80:80 $image_name