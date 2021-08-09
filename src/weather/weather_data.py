#!/bin/python3
import requests


def weather_data(city, key, unit=False):
    payload = [{
        "measurement": "weather",
        "time": "",
        "tags": {},
        "fields": {},
    }]

    url = "https://yahoo-weather5.p.rapidapi.com/weather"
    querystring = {"location": city, "format": "json", "u": unit}
    headers = {
        'x-rapidapi-key': key,
        'x-rapidapi-host': "yahoo-weather5.p.rapidapi.com"
        }

    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        # return weather data as a dict (json).
        resp = response.json()

        if resp is not None:
            for k, v in resp.items():
                # tags ################
                if k == "location":
                    for i in v:
                        city = v['city']
                        region = v['region']
                        timezone = v['timezone_id']

                        payload[0]["tags"]["city"] = city
                        payload[0]["tags"]["region"] = region
                        payload[0]["tags"]["timezone_id"] = timezone
                # fields ################
                if k == "current_observation":
                    for i in v:
                        wind_speed = round(float(v['wind']['speed']))
                        sunrise = v['astronomy']['sunrise']
                        sunset = v['astronomy']['sunset']

                        payload[0]["fields"]["wind_speed"] = wind_speed
                        payload[0]["fields"]["sunrise"] = sunrise
                        payload[0]["fields"]["sunset"] = sunset
                # fields + time ################
                if k == "forecasts":
                    for i in v:
                        day = i['day']
                        epoch = i['date']
                        low = round(float(i['low']))
                        high = round(float(i['high']))
                        condition = i['text']

                        payload[0]["time"] = epoch
                        payload[0]["fields"]["day"] = day
                        payload[0]["fields"]["low"] = low
                        payload[0]["fields"]["high"] = high
                        payload[0]["fields"]["condition"] = condition

    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout) as e:
        print(f"API Connectivity Error: {e}")

    return payload
