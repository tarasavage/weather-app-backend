from rest_framework import serializers
from userinteraction.models import FavoriteCity


class FavoriteCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteCity
        fields = ["id", "user", "city"]
