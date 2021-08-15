#!/bin/python3
import os
import logging
from influxdb import InfluxDBClient, exceptions as ex
"""
Script to initialize 'weather' database:
- pings the connection to influx db container.
- creates weather db if it doesn't exist.
"""


def init(username, password):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename="/weather/log/db_init.log", filemode="a")

    DB_HOST = os.getenv('DB_IP_ADDRESS')
    DB_PORT = os.getenv('DB_API_PORT')
    # PROD_DB_NAME = os.getenv('PROD_DB_NAME')
    TESTING_DB_NAME = os.getenv('TESTING_DB_NAME')

    try:
        client = InfluxDBClient(host=DB_HOST, port=DB_PORT, username=username, password=password, database=TESTING_DB_NAME)

        version = client.ping()
        logging.info("Successfully connected to InfluxDB: " + version)

        dbs = client.get_list_database()
        databases = {k for d in dbs for k in d.values()}
        if TESTING_DB_NAME not in databases:
            client.create_database(TESTING_DB_NAME)
            logging.info(f"DB {TESTING_DB_NAME} created successfully.")
        else:
            logging.info(f"DB already exist.")

        client.close()

    except (ex.InfluxDBClientError, ex.InfluxDBServerError) as e:
        logging.critical(f"Influxdb server side error: \n{e}")
    except Exception as j:
        logging.critical(f"Failed to establish a db connection: \n{j}")

