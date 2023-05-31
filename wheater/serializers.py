from rest_framework import serializers
from wheater.models import (
    City,
    DailyWeather,
    CurrentWeather,
    HourlyWeather
)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class WeatherSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        abstract = True
        fields = "__all__"


class DailyWeatherSerializer(WeatherSerializer):
    class Meta(WeatherSerializer.Meta):
        model = DailyWeather


class CurrentWeatherSerializer(WeatherSerializer):
    class Meta(WeatherSerializer.Meta):
        model = CurrentWeather


class HourlyWeatherSerializer(WeatherSerializer):
    class Meta(WeatherSerializer.Meta):
        model = HourlyWeather
