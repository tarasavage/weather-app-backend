from typing import Type
from datetime import datetime

import requests

from wheater.models import City, CurrentWeather

API_KEY = "5a1b11a7a00f6c06e792ed6bb1ee3cd2"


def get_nested_value(data, keys, default=None):
    for key in keys:
        if isinstance(data, list):
            try:
                index = int(key)
                data = data[index]
            except (ValueError, IndexError):
                return default
        else:
            data = data.get(key)
        if data is None:
            return default
    return data if data is not None else default


def scrape_city(city_name: str) -> City | None:
    url = (f"http://api.openweathermap.org/geo/1.0/"
           f"direct?q={city_name}&appid={API_KEY}")

    try:
        with requests.get(url) as response:
            if response.status_code == 200:
                coords_response = response.json()

                if (
                        isinstance(coords_response, list)
                        and len(coords_response) > 0
                ):
                    coords_response = coords_response[0]

                city = City(
                    name=coords_response.get("name", "London"),
                    lat=coords_response.get("lat", 51.5074),
                    lon=coords_response.get("lon", -0.1278),
                    country=coords_response.get("country", "GB")
                )

                city.save()

                return city
            else:
                print((f"Error: Request failed with status code "
                       f"{response.status_code}"))
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return None


def scrape_current_weather(city_name: str) -> Type[CurrentWeather] | None:
    city = scrape_city(city_name)

    if city is None:
        raise ValueError(f"Failed to fetch city data for '{city_name}'")

    url = (f"https://api.openweathermap.org/data/2.5/"
           f"weather?lat={city.lat}&lon={city.lon}"
           f"&appid={API_KEY}&units=metric")

    try:
        with requests.get(url) as response:
            if response.status_code == 200:
                cur_weather_response = response.json()

                if (
                        isinstance(cur_weather_response, list)
                        and len(cur_weather_response) > 0
                ):
                    cur_weather_response = cur_weather_response[0]
                elif not isinstance(cur_weather_response, dict):
                    raise ValueError("Unexpected response format")

                current_weather = CurrentWeather(
                    city=city,
                    dt=datetime.utcfromtimestamp(
                        get_nested_value(cur_weather_response, ["dt"], 0)
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                    temp=get_nested_value(
                        cur_weather_response, ["main", "temp"], 20.37
                    ),
                    feels_like=get_nested_value(
                        cur_weather_response, ["main", "feels_like"], 19.92
                    ),
                    pressure=get_nested_value(
                        cur_weather_response, ["main", "pressure"], 1016
                    ),
                    humidity=get_nested_value(
                        cur_weather_response, ["main", "humidity"], 56
                    ),
                    clouds=get_nested_value(
                        cur_weather_response, ["clouds", "all"], 74
                    ),
                    visibility=get_nested_value(
                        cur_weather_response, ["visibility"], 10000
                    ),
                    wind_speed=get_nested_value(
                        cur_weather_response, ["wind", "speed"], 3.09
                    ),
                    wind_deg=get_nested_value(
                        cur_weather_response, ["wind", "deg"], 220
                    ),
                    wind_gust=get_nested_value(
                        cur_weather_response, ["wind", "gust"]
                    ),
                    rain_1h=get_nested_value(
                        cur_weather_response, ["rain", "1h"]
                    ),
                    snow_1h=get_nested_value(
                        cur_weather_response, ["snow", "1h"]
                    ),
                    weather_id=get_nested_value(
                        cur_weather_response, ["weather", 0, "id"], 501
                    ),
                    weather_main=get_nested_value(
                        cur_weather_response,
                        ["weather", 0, "main"],
                        "Clouds"
                    ),
                    weather_description=get_nested_value(
                        cur_weather_response,
                        ["weather", 0, "description"],
                        "scattered clouds"
                    ),
                    weather_icon=get_nested_value(
                        cur_weather_response, ["weather", 0, "icon"], "03n"
                    ),
                )

                current_weather.save()

                return CurrentWeather
            else:
                print(
                    (f"Error: Request failed with status code "
                     f"{response.status_code}")
                )
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    raise ValueError(f"Failed to fetch current weather for '{city_name}'")
