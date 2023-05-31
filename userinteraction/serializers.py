from rest_framework import serializers
from userinteraction.models import FavoriteCity
from wheater.serializers import CitySerializer


class FavoriteCitySerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = FavoriteCity
        fields = ["id", "user", "city"]
