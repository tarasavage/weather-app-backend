from django.db import models
from user.models import User
from wheater.models import City


class FavoriteCity(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorite_cities_related"
    )
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.city.name}"
