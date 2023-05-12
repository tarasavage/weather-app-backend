from django.urls import path
from wheater.views import current_weather, daily_weather, hourly_weather

urlpatterns = [
    path("current/<str:city_name>/", current_weather, name="current-weather"),
    path("daily/<str:city_name>/", daily_weather, name="daily-weather"),
    path("hourly/<str:city_name>/", hourly_weather, name="hourly-weather"),
    path("current/", current_weather, name="current-weather-default"),
    path("daily/", daily_weather, name="daily-weather-default"),
    path("hourly/", hourly_weather, name="hourly-weather-default"),
]

app_name = "weather"
