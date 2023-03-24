#!/bin/bash

image_name=$1

# Stop existing container
docker rm $(docker ps -aq) -f || true

# Pull latest Docker image
docker pull $image_name

# Run the latest container
docker run -d --name my_space --restart always -p 80:80 -w /SWE573_Project $image_name sh -c "pip install -r requirements.txt && python manage.py runserver 0.0.0.0:80"