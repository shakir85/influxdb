#!/bin/python3
import requests


def weather_data(city, key, unit=False):
    # a metadata like for forecasts
    metadata = [{
        "measurement": "weather",
        "time": "",
        "tags": {},
        "fields": {},
    }]
    # list of dicts for 10 days forecasts
    forecasts = []

    url = "https://yahoo-weather5.p.rapidapi.com/weather"
    querystring = {"location": city, "format": "json", "u": unit}
    headers = {
        'x-rapidapi-key': key,
        'x-rapidapi-host': "yahoo-weather5.p.rapidapi.com"
        }

    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        # convert weather data to a dict (json).
        resp = response.json()

        if resp is not None:
            for k, v in resp.items():
                # tags ################
                if k == "location":
                    for i in v:
                        city = v['city']
                        region = v['region']
                        timezone = v['timezone_id']

                        metadata[0]["tags"]["city"] = city
                        metadata[0]["tags"]["region"] = region
                        metadata[0]["tags"]["timezone_id"] = timezone
                # fields ################
                if k == "current_observation":
                    for i in v:
                        wind_speed = round(float(v['wind']['speed']))
                        sunrise = v['astronomy']['sunrise']
                        sunset = v['astronomy']['sunset']

                        metadata[0]["fields"]["wind_speed"] = wind_speed
                        metadata[0]["fields"]["sunrise"] = sunrise
                        metadata[0]["fields"]["sunset"] = sunset

            # assemble weather forecasts
            for k, v in resp.items():
                if k == "forecasts":
                    for i in v:
                        forecasts.append(i)

    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout) as e:
        print(f"API Connectivity Error: {e}")

    return metadata, forecasts
