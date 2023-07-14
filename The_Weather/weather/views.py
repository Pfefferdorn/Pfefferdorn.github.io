import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

def toggle_unit(request):
    if 'unit' in request.session:
        del request.session['unit']
    else:
        request.session['unit'] = 'imperial'
    return redirect('index')


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units={}&APPID=3ba8bb7eb57f43cfa4fca274e7d2b9de'
    units = 'metric'

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['name']
            existing_city = City.objects.filter(name=city_name).exists()
            if not existing_city:
                response = requests.get(url.format(city_name, units)).json()
                if response.get('cod') == 200:
                    city = City(name=city_name)
                    city.save()

    form = CityForm()
    cities = City.objects.all()

    weather_data = []

    for city in cities:
        response = requests.get(url.format(city.name, units)).json()
        if response.get('cod') == 200:
            temperature = int(response['main']['temp'])
            temperature_feel = int(response['main']['feels_like'])
            temperature_min = int(response['main']['temp_min'])
            temperature_max = int(response['main']['temp_max'])
            if 'unit' in request.session:
                if request.session['unit'] == 'imperial':
                    temperature = celsius_to_fahrenheit(temperature)
                    temperature_feel = celsius_to_fahrenheit(temperature_feel)
                    temperature_min = celsius_to_fahrenheit(temperature_min)
                    temperature_max = celsius_to_fahrenheit(temperature_max)

            city_weather = {
                'city': city.name,
                'temperature': temperature,
                'temperature_max': temperature_max,
                'temperature_min': temperature_min,
                'temperature_feel': temperature_feel,
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon']
            }
            weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/weather.html', context)

def remove_city(request, city):
    City.objects.filter(name=city).delete()
    return redirect('index')

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32
