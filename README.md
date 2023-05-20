
# Weather App

This is a weather app that scrapes weather data from the OpenWeatherMap API. It is built using Django and Django Rest Framework, and utilizes Celery for data synchronization with the API.

## Features
- Retrieve current weather data for a specific city
- Retrieve daily weather forecast for a specific city
- Retrieve hourly weather forecast for a specific city
- Automatic data synchronization with the OpenWeatherMap API using Celery tasks

## Prerequisites
Before running the application, make sure you have the following:

- Python 3.7 or higher
- Docker and Docker Compose installed

## Getting Started

1. Copy the `.env.sample` file and create a new file named `.env`. Populate the `.env` file with all the required data (API keys, database credentials, etc.).

2. Build and run the application using Docker Compose:

```
docker-compose up --build
```

3. Create an admin user to access the Django admin interface and manage the application:

```
docker-compose run web python manage.py createsuperuser
```

4. Create a schedule for the Celery tasks to synchronize the weather data. This can be done through the Django admin interface. Access the admin interface at `http://localhost:8000/admin` and configure the desired schedules for the tasks.

5. Access the Weather App at `http://localhost:8000` and start exploring the available weather data endpoints.

