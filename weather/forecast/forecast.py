import requests
import numpy as np

__all__ = ['get_daily_forecast']


def get_api_key():
    key = ''
    try:
        f = open('./weather/forecast/api_key.txt', 'r')
        key = f.read()
        f.close()
    except Exception:
        print('No API key found. Go to https://www.weatherbit.io/ to get one.')

    return key


def request_forecast(city):
    url = "https://api.weatherbit.io/v2.0/forecast/hourly"
    query_string = {
        'key': get_api_key(),
        'hours': 12,
        'city': city,
        'lang': 'ru'
    }

    attempts = 5

    for i in range(attempts):
        try:
            return requests.request("GET", url, params=query_string)
        except Exception:
            if i < (attempts - 1):
                continue
            else:
                raise Exception('Weather API is unavailable')


def get_daily_forecast(city):
    resp = request_forecast(city)

    if not resp.status_code == 200:
        if resp.status_code == 204:
            return {'status': 'C'}
        else:
            return {'status': 'N'}

    resp = resp.json()['data']
    temp = []
    humidity = []
    pressure = []
    wind = []
    precip = []
    snow = []
    uv = []

    for hourly_forecast in resp:
        temp.append(hourly_forecast['temp'])
        humidity.append(hourly_forecast['rh'])
        pressure.append(hourly_forecast['pres'])
        wind.append(hourly_forecast['wind_spd'])
        precip.append(hourly_forecast['pop'])
        snow.append(hourly_forecast['snow'])
        uv.append(hourly_forecast['uv'])

    temp = np.array(temp)
    humidity = np.array(humidity)
    pressure = np.array(pressure)
    wind = np.array(wind)
    precip = np.array(precip)
    snow = np.array(snow)
    uv = np.array(uv)

    daily_forecast = {
        'temp': [int(temp.mean()), int(temp.std())],
        'humidity': [int(humidity.mean()), int(humidity.std())],
        'pressure': int(pressure.mean()),
        'uv': int(uv.mean()),
        'snow': int(snow.max()),
        'wind': int(wind.max()),
        'precip': int(precip.max()),
        'description': resp[4]['weather']['description'],
        'icon': resp[4]['weather']['icon'],
        'status': 'ok'
    }

    return daily_forecast
