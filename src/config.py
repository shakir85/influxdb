#!/bin/python3
from influxdb import InfluxDBClient

"""
Global db configs and inits here.
This script should only run once (e.g. at container startup)
and before executing db reads & writes.
"""


def init(db_name, db_client):
    """Initialization: create a database only if it doesn't exist"""
    dbs = db_client.get_list_database()
    databases = {k for d in dbs for k in d.values()}
    if db_name not in databases:
        db_client.create_database(db_name)
        print(f"DB {db_name} created successfully.")
    else:
        print(f"DB already exist.")