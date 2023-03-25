# ShareIt Social Media Platform

This project is a web application designed as a social media platform where users can create spaces, post content, and interact with each other. Users can join spaces based on their interests, create and share posts within those spaces, and follow other users. The platform offers features such as post recommendations, favorites, tags, badges, search, user profiles, and notifications.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Local Development Setup](#local-development-setup)
  - [Local Python Environment](#local-python-environment)
    - [Local Python Environment (Optional)](#local-python-environment-optional)
  - [Docker Container Environment](#docker-container-environment)
  - [Docker Compose Environment](#docker-compose-environment)  
  - [Database Migrations Warning](#database-migrations-warning)
- [Debugging Django Application](#debugging-django-application)
  - [Debugging with Visual Studio Code](#debugging-with-visual-studio-code)
  - [Debugging with PyCharm](#debugging-with-pycharm)
- [Contribution](#contribution)
- [License](#license)

## Features

- Create spaces with unique names and descriptions
- Join and leave spaces
- Post content with mandatory title, content, link, tag, and optional photo
- Follow and unfollow other users
- View recommendations, favorites, and followed users' posts
- Add and manage tags for posts
- Earn badges based on achievements
- Search for posts and spaces based on various criteria
- Edit user profiles
- Receive notifications for various events

## Requirements

- Python 3.x
- Django
- Docker (optional)
- Docker Compose (optional)

## Local Development Setup

Follow the instructions below to set up and run the local development environment.

1. Make sure you have Python and the required packages installed on your machine. Additionally, ensure that Docker and Docker Compose are installed if you plan to use the containerized local development setup.
2. Clone the repository to your local machine.
3. Copy the .env.example file to a new file named .env.

Bash

```bash
cp .env.example .env
```

Powershell

```powershell
Copy-Item .env.example -Destination .env
```

4. Update the .env file with the appropriate values for your local development setup. If you want to use the central MySQL database, make sure to set the correct DATABASE_URL.

### Local Python Environment

First install the required Python packages.

```bash
pip install -r requirements.txt
```

Then, run the following command to start the Django development server:

```bash
python manage.py runserver 0.0.0.0:8000
```

#### Local Python Environment (Optional)

Using a Python virtual environment is an optional but recommended approach, as it allows you to isolate the project's dependencies from your global Python environment. To create a virtual environment, follow these steps:

Install the virtualenv package if you haven't already:

```bash
pip install virtualenv
```

Create a new virtual environment in your project directory:

```bash
virtualenv venv
```

Activate the virtual environment:

- On macOS and Linux:

```bash
source venv/bin/activate
```

- On Windows:

```powershell
.\venv\Scripts\activate
```

Then follow the steps in the [Local Python Environment](#local-python-environment) section to install the required packages and run the project.

### Docker Container Environment

To run the project using a Docker container, first create a .env file in the root directory with the required variables. Use the .env.example file as a reference for the required variables. Then, build the Docker image:

```bash
docker build -t <your_image_name> .
```

Then run a Docker container with the following commands:

```bash
docker run -d --name my_space --restart always -p 8000:80 -w /SWE573_Project --env-file .env <your_image_name> sh -c "pip install -r requirements.txt && python manage.py runserver 0.0.0.0:80"
```

To stop the development environment, run the following command:

```bash
docker stop my_space
```

**Note**: You need to rebuild the Docker image and recreate the container every time you make changes to the code. The advantage of this approach is that it closely resembles the production environment.

### Docker Compose Environment

To run the project using Docker Compose, first create a .env file in the root directory with the required variables. Use the .env.example file as a reference for the required variables. Then, run the following command to start the services defined in docker-compose.yml:

```bash
docker-compose up
```

This will build the Docker image, create the containers for the Django app and the MySQL database, and start the Django development server on port 8000. This method is useful when you want to run the application with all its dependencies, such as the database server, in a local environment.

To stop the development environment, press Ctrl+C in the terminal running Docker Compose, or run the following command in a separate terminal:

```bash
docker-compose down
```

## Debugging Django Application

Debugging is an essential part of the development process. Below are instructions for setting up debugging for a Django application using Visual Studio Code and PyCharm.

Check the [Contribution Guide](.github/CONTRIBUTING.md) first.

### Debugging with Visual Studio Code

1. Install the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) for Visual Studio Code.

2. Open the project folder in Visual Studio Code.

3. Create a `launch.json` file in the `.vscode` folder with the following configuration:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Django",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/manage.py",
      "args": [
        "runserver"
      ],
      "django": true
    }
  ]
}
```

4. Set a breakpoint in the code where you want to start debugging.
5. Click the Debug icon in the Activity Bar on the left side of the window, then click the green play (or f5) button to start debugging.

For more information, check the official [Visual Studio Code documentation](https://code.visualstudio.com/docs/python/debugging).

### Debugging with PyCharm

1. Open the project folder in PyCharm.

2. Go to `Run` > `Edit` Configurations and add a new configuration for Django Server.

3. Fill in the required fields:

    - Name: Django Server
    - Script path: Path to your manage.py file
    - Parameters: runserver
4. Set breakpoints in your code by clicking on the left side of the line number.
5. Start the debugger by pressing Shift+F9 or clicking the green "play" button in the toolbar.

For more information, check the official [PyCharm documentation](https://www.jetbrains.com/help/pycharm/run-debug-configuration.html).

### Database Migrations Warning

**WARNING:** There is an ongoing work-in-progress process for handling database migrations in this project. Until then, **DO NOT** run the following commands when connected to the centralized database:

```bash
python manage.py makemigrations
python manage.py migrate
```

Please double-check your `.env` file before running these commands to ensure you are not accidentally making changes to the centralized database.

## Troubleshooting

If you encounter any issues during the local development setup or while working on the project, refer to the following common issues and their solutions:

### Issue: `python manage.py makemigrations` does not generate migration files for some projects

**Solution**: In some cases, running `python manage.py makemigrations` may not generate migration files for certain projects. If this happens, try running the command for individual projects, like this:

```bash
python manage.py makemigrations <project_name>
```

For example, if you want to generate migration files for the blog project, use the following command:

```bash
python manage.py makemigrations blog
```

### Issue: Unexpected problems when working with Docker containers

**Solution**: If you encounter unexpected issues while working with Docker containers, cleaning up the running containers and rebuilding them can be helpful. To remove all running containers, use the following command:

```bash
docker rm $(docker ps -aq) -f
```

Then, rebuild the Docker image and recreate the container using the instructions in the [Docker Container Environment](#docker-container-environment) section.

For Docker Compose, it will rebuild the containers automatically when you run docker-compose up. If you want to force a rebuild for Docker Compose, use the following command:

```bash
docker-compose up --build
```

## Contribution

Please refer to the [Contribution Guide](.github/CONTRIBUTING.md) for instructions on how to contribute to the project, including guidelines for creating branches, submitting pull requests, and working with JIRA for task management.

## License

Licensed under MIT, see [LICENSE](LICENSE) for the full text.
