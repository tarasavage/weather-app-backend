from rest_framework.response import Response
from rest_framework.decorators import api_view

from wheater.models import City, CurrentWeather, DailyWeather, HourlyWeather
from wheater.serializers import (
    DailyWeatherSerializer,
    CurrentWeatherSerializer,
    HourlyWeatherSerializer,
)
from wheater.scraper import (
    scrape_current_weather,
    scrape_daily_weather,
    scrape_hourly_weather
)
from django.conf import settings


@api_view(["GET"])
def current_weather(request, city_name=settings.DEFAULT_CITY_NAME):
    current_forecast = (
        CurrentWeather.objects.filter(city__name=city_name).last()
        if CurrentWeather.objects.filter(city__name=city_name).count()
        else scrape_current_weather(city_name)
    )
    serializer = CurrentWeatherSerializer(current_forecast)

    return Response(serializer.data)


@api_view(["GET"])
def daily_weather(request, city_name=settings.DEFAULT_CITY_NAME):
    daily_forecast = (
        DailyWeather.objects.filter(
            city__name=city_name
        ).order_by("-dt")[:7][::-1]
        if DailyWeather.objects.filter(city__name=city_name).count()
        else scrape_daily_weather(city_name)
    )
    serializer = DailyWeatherSerializer(daily_forecast, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def hourly_weather(request, city_name=settings.DEFAULT_CITY_NAME):
    hourly_forecast = (
        HourlyWeather.objects.filter(
            city__name=city_name
        ).order_by("-dt")[:24:3][::-1]
        if HourlyWeather.objects.filter(city__name=city_name).count()
        else scrape_hourly_weather(city_name)
    )
    serializer = HourlyWeatherSerializer(hourly_forecast, many=True)

    return Response(serializer.data)
