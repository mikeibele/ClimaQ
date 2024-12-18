import os
import requests
from dotenv import load_dotenv
from dataclasses import dataclass

# Load environment variables (API Key)
load_dotenv(dotenv_path=".env")
api_key = os.getenv("API_KEY")

@dataclass
class WeatherData:
    city: str
    temperature: int
    description: str
    icon: str
    high: int
    low: int

# Function to fetch latitude and longitude for a city
def get_lat_lon(city_name, state_code="", country_code="", API_KEY=api_key):
    try:
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_KEY}"
        response = requests.get(url).json()
        if response:
            data = response[0]
            return data.get("lat"), data.get("lon")
        return None, None
    except Exception as e:
        print(f"Error fetching coordinates: {e}")
        return None, None

# Function to fetch current weather data
def get_current_weather(lat, lon, API_KEY=api_key):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial"
        response = requests.get(url).json()
        main = response.get("main", {})
        weather = response.get("weather", [{}])[0]
        return WeatherData(
            city=response.get("name"),
            temperature=int(main.get("temp")),
            description=weather.get("description").capitalize(),
            icon=weather.get("icon"),
            high=int(main.get("temp_max")),
            low=int(main.get("temp_min"))
        )
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None

# Function to fetch user's location using IP
def get_user_location():
    try:
        location_data = requests.get("https://ipinfo.io").json()
        city = location_data.get("city", "")
        country = location_data.get("country", "")
        return city, country
    except Exception as e:
        print(f"Error detecting location: {e}")
        return None, None
