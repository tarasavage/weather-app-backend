from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from userinteraction.models import FavoriteCity
from wheater.models import City


class FavoriteCityView(APIView):
    def post(self, request, city_id):
        try:
            city = City.objects.get(id=city_id)
        except City.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if FavoriteCity.objects.filter(user=user, city=city).exists():
            return Response(status=status.HTTP_200_OK)

        FavoriteCity.objects.create(user=user, city=city)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, city_id):
        try:
            city = City.objects.get(id=city_id)
        except City.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user

        FavoriteCity.objects.filter(user=user, city=city).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
