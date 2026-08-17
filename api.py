from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WeatherApp:
    def __init__(self, city, lat, lon):
        self.city = city
        self.lat = lat
        self.lon = lon
        self.data = None

    def get_coords(self, city_name):
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            if "results" in data and len(data["results"]) > 0:
                lat = data["results"][0]["latitude"]
                lon = data["results"][0]["longitude"]
                return lat, lon
            else:
                return None, None

        except:
            return None, None

    def fetch_weather(self):
        
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={self.lat}&longitude={self.lon}"
            f"&current_weather=true"
            f"&hourly=relativehumidity_2m"
            f"&daily=temperature_2m_max,temperature_2m_min,windspeed_10m_max"
            f"&timezone=auto"
        )
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            self.data = response.json()
        except:
            self.data = None

    def get_weather(self):
       
        if not self.data or "current_weather" not in self.data:
            return {"error": "No weather data"}
        temp = self.data["current_weather"]["temperature"]
        return {"city":self.city, "temperature": temp}

    def get_humidity(self):
       
        if not self.data or "hourly" not in self.data:
            return {"error": "No humidity data"}
        humidity = self.data["hourly"]["relativehumidity_2m"][0]
        return {"humidity": humidity}

    def get_forecast(self):
           
            if not self.data or "daily" not in self.data:
                return {"error": "No forecast"}
            return {
                "max_temp": self.data["daily"]["temperature_2m_max"][0],
                "min_temp": self.data["daily"]["temperature_2m_min"][0]
            }

@app.get("/api/weather/{city}")
def get_weather_data(city: str):
    app = WeatherApp(city, 0, 0)
    lat, lon = app.get_coords(city)
    if lat is None:
        return{"error": "City not found"}

    app = WeatherApp(city, lat, lon)
    app.fetch_weather()

    if app.data is None:
        return {"error": "Failed to fetch weather"}

    return{
        "current": app.get_weather(),
        "humidity": app.get_humidity(),
        "forecast": app.get_forecast()
    }