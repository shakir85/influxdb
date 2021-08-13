#!/bin/python3
from datetime import datetime
from src.weather.weather_data import weather_data
from influxdb import InfluxDBClient, exceptions as ex
from argparse import ArgumentParser

# TODO add logging (replace print statements).

if __name__ == "__main__":

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    parser = ArgumentParser()
    parser.add_argument('-s', "--host",
                        type=str, required=True, help="Database IP or hostname (default is localhost) - (required).")
    parser.add_argument('-t', "--port", type=int, required=True, help="Database port (default is 8086) - (required).")
    parser.add_argument('-u', "--username", type=str, required=True, help="Database username - (required).")
    parser.add_argument('-p', "--password", type=str, required=True, help="Database password - (required).")
    parser.add_argument('-d', "--database", type=str, required=True, help="Target database - (required).")
    parser.add_argument('-c', "--city", type=str, required=True, help="City to get weather for - (required).")
    parser.add_argument('-k', "--api-key", type=str, required=True, help="API key - (required).")
    parser.add_argument('-n', "--unit", type=str, required=False,
                        help="Temperature units. 'f' for Fahrenheit or 'c' for Celsius, default is 'c' - (optional).")
    args = parser.parse_args()

    # Default temperature unit
    unit = "c"
    # Option to change temperature unit
    if args.unit:
        unit = args.unit

    # Get weather data. It is returned as a list of one dict.
    # This format is required by influx db.
    payload, forecasts = weather_data(city=args.city, key=args.api_key, unit=unit)

    # Create db client and write data.
    try:
        client = InfluxDBClient(host=args.host, port=args.port, username=args.username,password=args.password, database=args.database)

        for forecast in forecasts:
            day = forecast['day']
            epoch = forecast['date']
            low = round(float(forecast['low']))
            high = round(float(forecast['high']))
            condition = forecast['text']

            payload[0]["time"] = epoch
            payload[0]["fields"]["day"] = day
            payload[0]["fields"]["low"] = low
            payload[0]["fields"]["high"] = high
            payload[0]["fields"]["condition"] = condition

            client.write_points(payload)

        print(f"{now} - Payload data inserted to {args.database} DB.")
        client.close()

    except (ex.InfluxDBClientError, ex.InfluxDBServerError) as e:
        print(f"{now} - Failed to send metrics to influxdb {e}")
