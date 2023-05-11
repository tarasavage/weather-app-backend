from rest_framework import serializers
from wheater.models import (
    DailyWeather,
    CurrentWeather,
    HourlyWeather,
    City,
)


class DailyWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyWeather
        fields = "__all__"


class CurrentWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentWeather
        fields = "__all__"


class HourlyWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = HourlyWeather
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"
