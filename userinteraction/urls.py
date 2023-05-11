from django.urls import path
from userinteraction.views import FavoriteCityView

app_name = "userinteraction"

urlpatterns = [
    path(
        "cities/<int:city_id>/",
        FavoriteCityView.as_view(),
        name="favorite-city",
    ),
]
