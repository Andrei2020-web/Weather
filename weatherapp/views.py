from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm, NON_EXISTENT_CITY_ERROR
import requests
import os
from django.forms.utils import ErrorList


def home_page(request):
    '''домашня страница'''

    # API ключ можно получить по ссылке https://openweathermap.org/api
    api_key = os.environ.get('api_key_weather')
    all_cities = []
    citiesNames = []
    form = CityForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CityForm(request.POST)
            if form.is_valid():
                new_city = form.save(commit=False)
                new_city.owner = request.user
                new_city.save()
        else:
            if request.POST.get('name', ''):
                citiesNames.append(request.POST.get('name', ''))

    if request.user.is_authenticated:
        cities = City.objects.filter(owner=request.user).order_by('-id')
        for name in cities:
            citiesNames.append(name)

    for cityName in citiesNames:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={cityName}&appid={api_key}&units=metric'
        res = requests.get(url).json()
        if res.get('cod', '') == '404' or not res.get('cod', ''):
            form.errors["name"] = ErrorList([NON_EXISTENT_CITY_ERROR])
            if request.method == 'POST' and request.user.is_authenticated:
                new_city.delete()
            continue
        pressure_mm_rts = round(
            res["main"]["pressure"] * 0.750063755419211)
        city_info = {
            'name': cityName,
            'temp': res["main"]["temp"],
            'pressure': pressure_mm_rts,
            'humidity': res["main"]["humidity"],
            'wind': res["wind"]["speed"],
            'icon': res["weather"][0]["icon"],
        }
        all_cities.append(city_info)

    context = {'all_info': all_cities, 'form': form,
               'total_cities': len(all_cities)}
    return render(request, 'weatherapp/home.html',
                  context)


def delete_city(request, city_name):
    '''удаляет город из бд для пользователя'''
    pass
