import requests
from flask import Flask, render_template

app = Flask(__name__)

# Function to fetch weather data from OpenWeatherMap API
def fetch_weather_data(city):
    api_key = "b1b15e88fa797225412429c1c50c122a1"
    # Replace this with the actual OpenWeatherMap API endpoint for detailed forecast
    url = f"https://samples.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    
    # Process hourly weather for the next 24 hours
    hourly_weather = []
    for entry in data['list'][:8]:  # Assuming API provides 3-hour intervals, so 8 entries = 24 hours
        hourly_weather.append({
            'time': entry['dt_txt'].split(' ')[1][:5],  # Extract the time (HH:MM)
            'temp': int(entry['main']['temp'] - 273.15),  # Convert from Kelvin to Celsius
            'description': entry['weather'][0]['description'],
            'icon': f"https://openweathermap.org/img/wn/{entry['weather'][0]['icon']}@2x.png"
        })
    
    # Process daily weather for the next 7 days (static for now, as OpenWeatherMap free tier has limited daily data)
    daily_weather = [
        {
            'day': 'Monday',
            'temp': 25,
            'high': 28,
            'low': 22,
            'description': 'Clear sky',
            'icon': 'https://openweathermap.org/img/wn/01d@2x.png'
        },
        {
            'day': 'Tuesday',
            'temp': 24,
            'high': 27,
            'low': 21,
            'description': 'Partly cloudy',
            'icon': 'https://openweathermap.org/img/wn/03d@2x.png'
        },
        {
            'day': 'Wednesday',
            'temp': 22,
            'high': 24,
            'low': 20,
            'description': 'Rainy',
            'icon': 'https://openweathermap.org/img/wn/09d@2x.png'
        },
        {
            'day': 'Thursday',
            'temp': 23,
            'high': 26,
            'low': 19,
            'description': 'Thunderstorm',
            'icon': 'https://openweathermap.org/img/wn/11d@2x.png'
        },
        {
            'day': 'Friday',
            'temp': 21,
            'high': 23,
            'low': 18,
            'description': 'Cloudy',
            'icon': 'https://openweathermap.org/img/wn/04d@2x.png'
        },
        {
            'day': 'Saturday',
            'temp': 27,
            'high': 29,
            'low': 25,
            'description': 'Sunny',
            'icon': 'https://openweathermap.org/img/wn/01d@2x.png'
        },
        {
            'day': 'Sunday',
            'temp': 28,
            'high': 30,
            'low': 26,
            'description': 'Sunny',
            'icon': 'https://openweathermap.org/img/wn/01d@2x.png'
        }
    ]
    
    return hourly_weather, daily_weather

@app.route('/')
def index():
    other_weather = [
        {'city': 'New York', 'temperature': 76, 'description': 'Sunny', 'high': 79, 'low': 70},
        {'city': 'Los Angeles', 'temperature': 85, 'description': 'Clear', 'high': 88, 'low': 75},
        {'city': 'Chicago', 'temperature': 65, 'description': 'Cloudy', 'high': 68, 'low': 60},
        {'city': 'Miami', 'temperature': 90, 'description': 'Hot', 'high': 92, 'low': 85},
    ]
    return render_template('index.html', other_weather=other_weather)

@app.route('/weather/<city>')
def weather_detail(city):
    hourly_weather, daily_weather = fetch_weather_data(city)
    return render_template(
        'weather_detail.html',
        city=city,
        hourly_weather=hourly_weather,
        daily_weather=daily_weather
    )

if __name__ == '__main__':
    app.run(debug=True)
