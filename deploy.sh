#!/bin/bash

image_name=$1
django_env=$2
secret_key=$3
debug=$4
allowed_hosts=$5
database_url=$6

# Stop existing container
docker rm $(docker ps -aq) -f || true

# Pull latest Docker image
docker pull $image_name

# Create a volume for the uploaded images
docker volume create my_space_images

# Run the latest container
docker run -d --name my_space --restart always -p 80:80 -w /SWE573_Project -e DJANGO_ENV="$django_env" -e SECRET_KEY="$secret_key" -e DEBUG="$debug" -e ALLOWED_HOSTS="$allowed_hosts" -e DATABASE_URL="$database_url" -v my_space_images:/SWE573_Project/media $image_name sh -c "pip install -r requirements.txt && python manage.py runserver 0.0.0.0:80"
