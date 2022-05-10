import rumps
import json
import requests
import GetIcon
import os

class main():
    def get_user_region(self):
        # Get user IP address
        result = os.popen("curl ifconfig.me").read()
        print(result)
        # Get user region using their IP address
        url = requests.get(f'https://ipapi.co/{result}/json/?key={add your own key here}')
        data = json.loads(url.text)
        print(data)
        return data['region']

    def load_api_data(self):
        region = self.get_user_region()
        url = requests.get(f'http://api.weatherapi.com/v1/forecast.json?key={add your own key here}&q=london&days=1&aqi=no&alerts=no')
        data = json.loads(url.text)
        return data

    def WeatherData(self, data_object):
        location = data_object['location']['name']
        condition = data_object['current']['condition']['text']

        temp_c = data_object['current']['temp_c']
        wind = data_object['current']['wind_mph']
        humidity = data_object['current']['humidity']
        feels_like_c = data_object['current']['feelslike_c']
        uv = data_object['current']['uv']
        icon = data_object['current']['condition']['icon']

        return location, condition, wind, feels_like_c, uv, icon, temp_c

    def Determine_UV_Level(self, uv_value):
        if 1 <= uv_value <= 2:
            return "Low 🟢"
        elif 3 <= uv_value <= 5:
            return "Moderate 🟡"
        elif 6 <= uv_value <= 7:
            return "HIGH 🟠"
        elif 8 <= uv_value <= 11:
            return "VERY HIGH 🔴"

test = main()
api_data = test.load_api_data()
weather_data = test.WeatherData(api_data)
listofmenuitems = [f"Wind: {weather_data[2]} mph", f"Feels like: {weather_data[3]}˚C", f"UV: {int(weather_data[4])} {test.Determine_UV_Level(weather_data[4])}"]
icon_path = GetIcon.return_icon(weather_data[5])

class WeatherBarApp(rumps.App):
    def __init__(self):
        super(WeatherBarApp, self).__init__("Weather Bar App", icon=icon_path)
        self.title = f"{weather_data[1]} {int(weather_data[-1])}˚C"
        self.menu = listofmenuitems
        self.wind = rumps.MenuItem(title=f"{weather_data[2]}")


    @rumps.timer(3600)
    def refreshApp(self, _):
        test = main()
        api_data = test.load_api_data()
        weather_data = test.WeatherData(api_data)
        listofmenuitems = [f"Wind: {weather_data[2]} mph", f"Feels like: {weather_data[3]}˚C", f"UV: {int(weather_data[4])} {test.Determine_UV_Level(weather_data[4])}"]
        icon_path = GetIcon.return_icon(weather_data[5])

        print("-")

if __name__ == "__main__":
    WeatherBarApp().run()
