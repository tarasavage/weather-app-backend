from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from celery import shared_task
from django.db.models import Q
from datetime import date

from wheater.models import DailyWeather


@shared_task
def send_notification_emails() -> None:
    users = get_user_model().objects.filter(notification=True)
    current_date = date.today()

    for user in users:
        favorite_cities = user.favorite_cities.all()

        cities_info = []
        for city in favorite_cities:
            daily_forecast = DailyWeather.objects.get(
                Q(dt__date=current_date) & Q(city=city)
            )

            if daily_forecast:
                city_info = (
                    f"City: {city.name}\n"
                    f"Max temperature: {daily_forecast.temp_max}°C\n"
                    f"Weather description: "
                    f"{daily_forecast.weather_description}\n"
                )
                cities_info.append(city_info)

        message = "This is your daily notification.\n\n"
        message += "Favorite Cities:\n"
        message += "\n".join(cities_info)

        send_mail(
            subject="Daily Notification",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=True,
        )
