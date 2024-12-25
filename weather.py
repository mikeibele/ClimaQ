import os
import requests
from dotenv import load_dotenv
from dataclasses import dataclass

# Load API key from .env file
load_dotenv(dotenv_path=".env")
api_key = os.getenv("API_KEY")

@dataclass
class WeatherData:
    city: str
    temperature: int
    description: str
    high: int
    low: int

# Function to get latitude and longitude
def get_lat_lon(city_name, API_KEY=api_key):
    try:
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={API_KEY}"
        response = requests.get(url).json()
        if response:
            return response[0]["lat"], response[0]["lon"]
        return None, None
    except Exception as e:
        print(f"Error fetching coordinates: {e}")
        return None, None

# Fetch current weather
def get_current_weather(lat, lon, API_KEY=api_key):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial"
        response = requests.get(url).json()
        weather = response["weather"][0]
        main = response["main"]
        return WeatherData(
            city=response["name"],
            temperature=int(main["temp"]),
            description=weather["description"].capitalize(),
            high=int(main["temp_max"]),
            low=int(main["temp_min"])
        )
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None

# Fetch hourly forecast
def get_hourly_forecast(lat, lon, API_KEY=api_key):
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial"
        response = requests.get(url).json()
        return [
            {"time": item["dt_txt"], "temp": item["main"]["temp"], "description": item["weather"][0]["description"]}
            for item in response["list"][:8]
        ]
    except Exception as e:
        print(f"Error fetching hourly forecast: {e}")
        return []

# Fetch daily forecast
def get_daily_forecast(lat, lon, API_KEY=api_key):
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt=7&appid={API_KEY}&units=imperial"
        response = requests.get(url).json()
        return [
            {"day": item["dt"], "temp": item["temp"]["day"], "high": item["temp"]["max"], "low": item["temp"]["min"], "description": item["weather"][0]["description"]}
            for item in response["list"]
        ]
    except Exception as e:
        print(f"Error fetching daily forecast: {e}")
        return []
