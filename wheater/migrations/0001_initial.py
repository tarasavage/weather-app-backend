# Generated by Django 4.2 on 2023-05-31 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="City",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("lat", models.FloatField()),
                ("lon", models.FloatField()),
                ("country", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="HourlyWeather",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("dt", models.DateTimeField()),
                ("pressure", models.FloatField()),
                ("humidity", models.FloatField()),
                ("clouds", models.FloatField()),
                ("wind_speed", models.FloatField()),
                ("wind_gust", models.FloatField(null=True)),
                ("wind_deg", models.FloatField()),
                ("weather_id", models.IntegerField()),
                ("weather_main", models.CharField(max_length=100)),
                ("weather_description", models.CharField(max_length=100)),
                ("weather_icon", models.CharField(max_length=50)),
                ("temp", models.FloatField()),
                ("feels_like", models.FloatField()),
                ("temp_min", models.FloatField()),
                ("temp_max", models.FloatField()),
                ("sea_level", models.FloatField()),
                ("ground_level", models.FloatField()),
                ("pop", models.FloatField()),
                ("visibility", models.FloatField()),
                ("rain_1h", models.FloatField(null=True)),
                ("snow_1h", models.FloatField(null=True)),
                (
                    "city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="wheater.city"
                    ),
                ),
            ],
            options={
                "abstract": False,
                "unique_together": {("city", "dt")},
            },
        ),
        migrations.CreateModel(
            name="DailyWeather",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("dt", models.DateTimeField()),
                ("pressure", models.FloatField()),
                ("humidity", models.FloatField()),
                ("clouds", models.FloatField()),
                ("wind_speed", models.FloatField()),
                ("wind_gust", models.FloatField(null=True)),
                ("wind_deg", models.FloatField()),
                ("weather_id", models.IntegerField()),
                ("weather_main", models.CharField(max_length=100)),
                ("weather_description", models.CharField(max_length=100)),
                ("weather_icon", models.CharField(max_length=50)),
                ("sunrise", models.DateTimeField()),
                ("sunset", models.DateTimeField()),
                ("temp_min", models.FloatField()),
                ("temp_max", models.FloatField()),
                ("temp_morn", models.FloatField()),
                ("temp_day", models.FloatField()),
                ("temp_eve", models.FloatField()),
                ("temp_night", models.FloatField()),
                ("feels_like_morn", models.FloatField()),
                ("feels_like_day", models.FloatField()),
                ("feels_like_eve", models.FloatField()),
                ("feels_like_night", models.FloatField()),
                ("pop", models.FloatField()),
                ("rain", models.FloatField(null=True)),
                ("snow", models.FloatField(null=True)),
                (
                    "city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="wheater.city"
                    ),
                ),
            ],
            options={
                "abstract": False,
                "unique_together": {("city", "dt")},
            },
        ),
        migrations.CreateModel(
            name="CurrentWeather",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("dt", models.DateTimeField()),
                ("pressure", models.FloatField()),
                ("humidity", models.FloatField()),
                ("clouds", models.FloatField()),
                ("wind_speed", models.FloatField()),
                ("wind_gust", models.FloatField(null=True)),
                ("wind_deg", models.FloatField()),
                ("weather_id", models.IntegerField()),
                ("weather_main", models.CharField(max_length=100)),
                ("weather_description", models.CharField(max_length=100)),
                ("weather_icon", models.CharField(max_length=50)),
                ("temp", models.FloatField()),
                ("feels_like", models.FloatField()),
                ("visibility", models.FloatField()),
                ("rain_1h", models.FloatField(null=True)),
                ("snow_1h", models.FloatField(null=True)),
                (
                    "city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="wheater.city"
                    ),
                ),
            ],
            options={
                "abstract": False,
                "unique_together": {("city", "dt")},
            },
        ),
    ]
