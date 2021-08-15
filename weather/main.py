#!/bin/python3
import os
import logging
import time
import schedule
import weather_data
import db_init
from datetime import datetime
from influxdb import InfluxDBClient, exceptions as ex
from argparse import ArgumentParser

# TODO: Enhance logging -> add debug mode logs.


def main(username, password, api_key):
    # Environment variables should be exported via compose file.
    DB_HOST = os.getenv('DB_IP_ADDRESS')
    DB_PORT = os.getenv('DB_API_PORT')
    CITY = os.getenv('CITY')
    PROD_DB_NAME = os.getenv('PROD_DB_NAME')
    TESTING_DB_NAME = os.getenv('TESTING_DB_NAME')

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename="/weather/log/main.log", filemode="a")

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get weather data. It is returned as a list of a one dict.
    # this format is required by influx db.
    payload, forecasts = weather_data.weather_data(city=CITY, key=api_key, unit="c")

    # Create db client and write data.
    try:
        client = InfluxDBClient(host=DB_HOST, port=DB_PORT, username=username, password=password,
                                database=TESTING_DB_NAME)

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

        logging.info(f"Payload data inserted to {DB_HOST} DB.")
        client.close()

    except (ex.InfluxDBClientError, ex.InfluxDBServerError) as e:
        logging.critical(f"Influxdb server side error: \n{e}")
    except Exception as j:
        logging.critical(f"Failed to establish a db connection: \n{j}")


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument('-u', "--username", type=str, required=True, help="Database username - (required).")
    parser.add_argument('-p', "--password", type=str, required=True, help="Database password - (required).")
    parser.add_argument('-k', "--api-key", type=str, required=True, help="API key - (required).")

    args = parser.parse_args()

    db_init.init(username=args.username, password=args.password)

    time.sleep(5)

    schedule.every(2).minutes.do(main, username=args.username, password=args.password, api_key=args.api_key)
    # schedule.every().day.at("6:00").do(main, username=args.username, password=args.password, api_key=args.api_key)
    while True:
        schedule.run_pending()
