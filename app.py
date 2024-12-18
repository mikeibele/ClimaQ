from flask import Flask, render_template, request
from weather import get_user_location, get_lat_lon, get_current_weather

app = Flask(__name__)

# Predefined list of cities
predefined_cities = [
    {"name": "San Francisco", "country": "US"},
    {"name": "Seattle", "country": "US"},
    {"name": "Miami", "country": "US"},
    {"name": "London", "country": "UK"},
    {"name": "Los Angeles", "country": "US"}
]

@app.route("/", methods=["GET", "POST"])
def home():
    # Fetch weather for user's location
    user_city, user_country = get_user_location()
    if user_city and user_country:
        lat, lon = get_lat_lon(user_city, country_code=user_country)
        my_location_weather = get_current_weather(lat, lon) if lat and lon else None
    else:
        my_location_weather = None

    # Fetch weather for predefined cities
    other_weather = []
    for city in predefined_cities:
        lat, lon = get_lat_lon(city["name"], country_code=city["country"])
        if lat and lon:
            weather_data = get_current_weather(lat, lon)
            if weather_data:
                other_weather.append(weather_data)

    # Handle search bar functionality
    search_result = None
    if request.method == "POST":
        search_query = request.form.get("search")
        if search_query:
            lat, lon = get_lat_lon(search_query)
            if lat and lon:
                search_result = get_current_weather(lat, lon)

    return render_template(
        "index.html",
        my_location=my_location_weather,
        other_weather=other_weather,
        search_result=search_result
    )

if __name__ == "__main__":
    app.run(debug=True)
