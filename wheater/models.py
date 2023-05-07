from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    timezone = models.CharField(max_length=100)
    timezone_offset = models.IntegerField()

    def __str__(self):
        return self.name


class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    dt = models.DateTimeField()
    temp = models.DecimalField(max_digits=5, decimal_places=2)
    feels_like = models.DecimalField(max_digits=5, decimal_places=2)
    pressure = models.DecimalField(max_digits=6, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    dew_point = models.DecimalField(max_digits=5, decimal_places=2)
    clouds = models.DecimalField(max_digits=5, decimal_places=2)
    uvi = models.DecimalField(max_digits=5, decimal_places=2)
    visibility = models.DecimalField(max_digits=6, decimal_places=2)
    wind_speed = models.DecimalField(max_digits=6, decimal_places=2)
    wind_gust = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    wind_deg = models.DecimalField(max_digits=6, decimal_places=2)
    rain_1h = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    snow_1h = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    class Meta:
        abstract = True


class CurrentWeather(Weather):
    def __str__(self):
        return f"Current weather for {self.city.name} at {self.dt}"


class HourlyWeather(Weather):
    pop = models.DecimalField(max_digits=5, decimal_places=2)  # probability of precipitation
    weather_id = models.IntegerField()
    weather_main = models.CharField(max_length=100)  # "Rain"
    weather_description = models.CharField(max_length=100)  # "light rain"
    weather_icon = models.CharField(max_length=50)  # "10n"

    def __str__(self):
        return f"Hourly weather for {self.city.name} at {self.dt}"


class DailyWeather(Weather):
    sunrise = models.DateTimeField()
    sunset = models.DateTimeField()
    moonrise = models.DateTimeField()
    moonset = models.DateTimeField()
    moon_phase = models.DecimalField(max_digits=3, decimal_places=2)
    temp_morn = models.DecimalField(max_digits=5, decimal_places=2)
    temp_day = models.DecimalField(max_digits=5, decimal_places=2)
    temp_eve = models.DecimalField(max_digits=5, decimal_places=2)
    temp_night = models.DecimalField(max_digits=5, decimal_places=2)
    feels_like_morn = models.DecimalField(max_digits=5, decimal_places=2)
    feels_like_day = models.DecimalField(max_digits=5, decimal_places=2)
    feels_like_eve = models.DecimalField(max_digits=5, decimal_places=2)
    feels_like_night = models.DecimalField(max_digits=5, decimal_places=2)
    pop = models.DecimalField(max_digits=5, decimal_places=2)
    rain = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    snow = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def __str__(self):
        return f"Daily weather for {self.city.name} on {self.dt}"
