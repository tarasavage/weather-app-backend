from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from wheater.models import City, DailyWeather, CurrentWeather, HourlyWeather
from wheater.serializers import (
    DailyWeatherSerializer,
    CurrentWeatherSerializer,
    HourlyWeatherSerializer,
)


DEFAULT_CITY_NAME = "Lviv"


@api_view(["GET"])
def current_weather(request, city_name=DEFAULT_CITY_NAME):
    city = get_object_or_404(City, name=city_name)
    current_forecast = CurrentWeather.objects.filter(city=city)
    serializer = CurrentWeatherSerializer(current_forecast, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def daily_weather(request, city_name=DEFAULT_CITY_NAME):
    city = get_object_or_404(City, name=city_name)
    daily_forecast = DailyWeather.objects.filter(city=city)
    serializer = DailyWeatherSerializer(daily_forecast, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def hourly_weather(request, city_name=DEFAULT_CITY_NAME):
    city = get_object_or_404(City, name=city_name)
    hourly_forecast = HourlyWeather.objects.filter(city=city)
    serializer = HourlyWeatherSerializer(hourly_forecast, many=True)

    return Response(serializer.data)
