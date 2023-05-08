# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.8

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /SWE574_Team2_Project

# Set the working directory to /SWE574_Team2_Project
WORKDIR /SWE574_Team2_Project

# Copy the current directory contents into the container at /SWE574_Team2_Project
ADD . /SWE574_Team2_Project/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
