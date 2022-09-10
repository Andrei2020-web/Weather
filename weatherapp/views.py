from django.shortcuts import render
import requests
import os


def home_page(request):
    '''домашня страница'''

    # API ключ можно получить по ссылке https://openweathermap.org/api
    api_key = os.environ.get('api_key_weather')

    if request.method == 'POST':
        city_name = request.POST.get('new_city', '')
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
        res = requests.get(url).json()
        pressure_mm_rts = round(res["main"]["pressure"] * 0.750063755419211)
        city_info = {
            'city': city_name,
            'temp': res["main"]["temp"],
            'pressure': pressure_mm_rts,
            'humidity': res["main"]["humidity"],
            'wind': res["wind"]["speed"],
            'icon': res["weather"][0]["icon"],
        }
        return render(request, 'weatherapp/home.html', city_info)
    return render(request, 'weatherapp/home.html')
