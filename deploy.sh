#!/bin/bash

image_name=$1
repo_path=$2

# Authencticate to AWS ECR
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin $repo_path

# Stop existing container
docker rm $(docker ps -aq) -f || true

# Pull latest Docker image
docker pull $image_name

# Run the latest container
$ docker run -d --name my_space --restart always -p 80:80 $image_name -w /SWE573_Project $image_name sh -c "pip install -r requirements.txt && python manage.py runserver 0.0.0.0:80"