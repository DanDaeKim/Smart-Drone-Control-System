# pip install requests

import requests

class WeatherIntegration:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather_data(self, latitude, longitude):
        params = {
            'lat': latitude,
            'lon': longitude,
            'appid': self.api_key,
            'units': 'metric'
        }

        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            weather_data = response.json()
            return weather_data
        else:
            raise ValueError(f"Failed to fetch weather data. Status code: {response.status_code}")

    def get_wind_data(self, latitude, longitude):
        weather_data = self.get_weather_data(latitude, longitude)
        wind_data = weather_data['wind']
        return wind_data

    def get_temperature(self, latitude, longitude):
        weather_data = self.get_weather_data(latitude, longitude)
        temperature_data = weather_data['main']
        return temperature_data['temp']

api_key = 'your_openweathermap_api_key'
weather_integration = WeatherIntegration(api_key)

latitude = 40.7128
longitude = -74.0060

wind_data = weather_integration.get_wind_data(latitude, longitude)
print(f"Wind data: {wind_data}")

temperature = weather_integration.get_temperature(latitude, longitude)
print(f"Temperature: {temperature} °C")

