from datetime import datetime

import requests

from wheater.models import City, CurrentWeather, DailyWeather, HourlyWeather, Weather

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


def get_response_from_api(url: str) -> dict | None:
    try:
        with requests.get(url) as response:
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: Request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return None


def save_obj_to_db(obj: City | Weather) -> None:
    try:
        obj.save()
    except Exception as e:
        print(f"Error while saving object to the database: {e}")


def create_city(coords_response: dict) -> City | None:
    if isinstance(coords_response, list) and len(coords_response) > 0:
        coords_response = coords_response[0]

    city = City(
        name=coords_response.get("name", "London"),
        lat=coords_response.get("lat", 51.5074),
        lon=coords_response.get("lon", -0.1278),
        country=coords_response.get("country", "GB")
    )

    return city


def get_city_from_db(city_name: str) -> City | None:
    try:
        city = City.objects.get(name=city_name)
        return city
    except City.DoesNotExist:
        return None


def scrape_city(city_name: str) -> City | None:
    try:
        city = get_city_from_db(city_name)

        if city:
            return city

    except Exception as e:
        print(f"Error while accessing the database: {e}")

    url = (f"http://api.openweathermap.org/geo/1.0/"
           f"direct?q={city_name}&appid={API_KEY}")

    try:
        coords_response = get_response_from_api(url)

        if coords_response:
            city = create_city(coords_response)

            if city:
                save_obj_to_db(city)
                return city

    except Exception as e:
        print(f"Error while accessing the API: {e}")

    return None


def create_current_weather(city: City, response: dict) -> CurrentWeather:
    if isinstance(response, list) and len(response) > 0:
        response = response[0]
    elif not isinstance(response, dict):
        raise ValueError("Unexpected response format")

    current_weather = CurrentWeather(
        city=city,
        dt=datetime.utcfromtimestamp(
            get_nested_value(response, ["dt"], 0)
        ).strftime("%Y-%m-%d %H:%M:%S"),
        temp=get_nested_value(response, ["main", "temp"], 20.37),
        feels_like=get_nested_value(response, ["main", "feels_like"], 19.92),
        pressure=get_nested_value(response, ["main", "pressure"], 1016),
        humidity=get_nested_value(response, ["main", "humidity"], 56),
        clouds=get_nested_value(response, ["clouds", "all"], 74),
        visibility=get_nested_value(response, ["visibility"], 10000),
        wind_speed=get_nested_value(response, ["wind", "speed"], 3.09),
        wind_deg=get_nested_value(response, ["wind", "deg"], 220),
        wind_gust=get_nested_value(response, ["wind", "gust"]),
        rain_1h=get_nested_value(response, ["rain", "1h"]),
        snow_1h=get_nested_value(response, ["snow", "1h"]),
        weather_id=get_nested_value(response, ["weather", 0, "id"], 501),
        weather_main=get_nested_value(response, ["weather", 0, "main"], "Clouds"),
        weather_description=get_nested_value(
            response, ["weather", 0, "description"], "scattered clouds"
        ),
        weather_icon=get_nested_value(response, ["weather", 0, "icon"], "03n"),
    )

    return current_weather


def scrape_current_weather(city_name: str) -> CurrentWeather | None:
    city = scrape_city(city_name)

    url = (f"https://api.openweathermap.org/data/2.5/"
           f"weather?lat={city.lat}&lon={city.lon}"
           f"&appid={API_KEY}&units=metric")

    try:
        cur_weather_response = get_response_from_api(url)

        current_weather = create_current_weather(city, cur_weather_response)

        return current_weather
    except Exception as e:
        print(f"Error: {e}")

    raise ValueError(f"Failed to fetch current weather for '{city_name}'")


def sync_current_weather_with_api(city_name: str) -> None:
    cur_weather = scrape_current_weather(city_name)
    save_obj_to_db(cur_weather)


def create_daily_weather(city: City, response: dict) -> DailyWeather:
    dt = datetime.fromtimestamp(get_nested_value(response, ["dt"], 0))

    daily_weather = DailyWeather(
        city=city,
        dt=dt.strftime("%Y-%m-%d %H:%M:%S"),
        pressure=get_nested_value(response, ["pressure"], 1016),
        humidity=get_nested_value(response, ["humidity"], 56),
        clouds=get_nested_value(response, ["clouds"], 74),
        wind_speed=get_nested_value(response, ["speed"], 3.09),
        wind_deg=get_nested_value(response, ["deg"], 220),
        wind_gust=get_nested_value(response, ["gust"]),
        weather_id=get_nested_value(response, ["weather", 0, "id"], 501),
        weather_main=get_nested_value(response, ["weather", 0, "main"], "Clouds"),
        weather_description=get_nested_value(response, ["weather", 0, "description"], "scattered clouds"),
        weather_icon=get_nested_value(response, ["weather", 0, "icon"], "03n"),
        sunrise=datetime.fromtimestamp(response.get("sunrise")),
        sunset=datetime.fromtimestamp(response.get("sunset")),
        temp_min=get_nested_value(response, ["temp", "min"], 20),
        temp_max=get_nested_value(response, ["temp", "max"], 20),
        temp_morn=get_nested_value(response, ["temp", "morn"], 20),
        temp_day=get_nested_value(response, ["temp", "day"], 20),
        temp_eve=get_nested_value(response, ["temp", "eve"], 20),
        temp_night=get_nested_value(response, ["temp", "night"], 20),
        feels_like_morn=get_nested_value(response, ["feels_like", "morn"], 20),
        feels_like_day=get_nested_value(response, ["feels_like", "day"], 20),
        feels_like_eve=get_nested_value(response, ["feels_like", "eve"], 20),
        feels_like_night=get_nested_value(response, ["feels_like", "night"], 20),
        pop=response.get("pop", 0.5),
        rain=response.get("rain", None),
        snow=response.get("snow", None),
    )

    return daily_weather


def scrape_daily_weather(city_name: str) -> list[DailyWeather] | None:
    city = scrape_city(city_name)

    url = (f"https://api.openweathermap.org/data/2.5/forecast/daily?"
           f"lat={city.lat}&lon={city.lon}&cnt=7&appid={API_KEY}")

    try:
        daily_weather_response = get_response_from_api(url)

        data = daily_weather_response.get("list", {})

        forecast = []

        for day in data:
            daily_weather = create_daily_weather(city, day)
            forecast.append(daily_weather)

        return forecast

    except Exception as e:
        print(f"Error: {e}")

    raise ValueError(f"Failed to fetch current weather for '{city_name}'")


def sync_daily_weather_with_api(city_name: str) -> None:
    forecast = scrape_daily_weather(city_name)

    for day in forecast:
        save_obj_to_db(day)


def create_hourly_weather(city: City, response: dict) -> HourlyWeather:
    dt = datetime.fromtimestamp(get_nested_value(response, ["dt"], 0))

    hourly_weather = HourlyWeather(
        city=city,
        dt=dt.strftime("%Y-%m-%d %H:%M:%S"),
        pressure=get_nested_value(response, ["pressure"], 1016),
        humidity=get_nested_value(response, ["humidity"], 56),
        clouds=get_nested_value(response, ["clouds", "all"], 74),
        wind_speed=get_nested_value(response, ["speed"], 3.09),
        wind_deg=get_nested_value(response, ["deg"], 220),
        wind_gust=get_nested_value(response, ["gust"]),
        weather_id=get_nested_value(response, ["weather", 0, "id"], 501),
        weather_main=get_nested_value(response, ["weather", 0, "main"], "Clouds"),
        weather_description=get_nested_value(response, ["weather", 0, "description"], "scattered clouds"),
        weather_icon=get_nested_value(response, ["weather", 0, "icon"], "03n"),
        temp=get_nested_value(response, ["main", "temp"], 20.37),
        feels_like=get_nested_value(response, ["main", "feels_like"], 19.92),
        temp_min=get_nested_value(response, ["main", "temp_min"], 20.37),
        temp_max=get_nested_value(response, ["main", "temp_max"], 27.5),
        sea_level=get_nested_value(response, ["main", "sea_level"], 1014),
        ground_level=get_nested_value(response, ["main", "ground_level"], 931),
        rain_1h=get_nested_value(response, ["rain", "1h"]),
        snow_1h=get_nested_value(response, ["snow", "1h"]),
        visibility=get_nested_value(response, ["visibility"]),
        pop=get_nested_value(response, ["pop"]),
    )

    return hourly_weather


def scrape_hourly_weather(city_name: str) -> list[HourlyWeather] | None:
    city = scrape_city(city_name)

    url = (f"https://pro.openweathermap.org/data/2.5/forecast/hourly?"
           f"lat={city.lat}&lon={city.lon}&appid={API_KEY}")

    try:
        hourly_weather_response = get_response_from_api(url)

        data = hourly_weather_response.get("list", {})

        forecast = []

        for day in data:
            hourly_weather = create_hourly_weather(city, day)
            forecast.append(hourly_weather)

        return forecast

    except Exception as e:
        print(f"Error: {e}")

    raise ValueError(f"Failed to fetch current weather for '{city_name}'")


def sync_hourly_weather_with_api(city_name: str) -> None:
    forecast = scrape_hourly_weather(city_name)

    for day in forecast:
        save_obj_to_db(day)
