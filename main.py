#!/bin/python3
from influxdb import InfluxDBClient
from argparse import ArgumentParser


def init(db_name, db_client):
    """Initialization: create the database only if it doesn't exist"""
    dbs = db_client.get_list_database()
    databases = {k for d in dbs for k in d.values()}
    if db_name not in databases:
        db_client.create_database(db_name)
        print(f"DB {db_name} created successfully.")
    else:
        print(f"DB already exist.")


def weather(weather_data):
    # client.write_points(points=weather_data, time_precision=now, database='weather_db')
    pass


def stocks():
    pass


def whatever():
    pass


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-s', "--host",
                        type=str, required=True, help="Database IP address or hostname (default is localhost).")
    parser.add_argument('-t', "--port",
                        type=int, required=True, help="Database port number (default is 8086).")
    parser.add_argument('-u', "--username",
                        type=str, required=True, help="Database username - (required).")
    parser.add_argument('-p', "--password",
                        type=str, required=True, help="Database password - (required).")
    parser.add_argument('-d', "--database",
                        type=str, required=False, help="Use only if you want to create a  db client for a specific database (discouraged).")
    parser.add_argument("--test-connection", required=False, default=False,
                        type=str, action='store_true', help="Test connection to influx_db before trying to create a db client (optional - not implemented yet).")
    args = parser.parse_args()

    # 2. get read data
    # 3. write to db

    client = InfluxDBClient(host=args.host, port=args.port, username=args.username, password=args.password)

    init('example', client)

    # Close db client after method calls
    client.close()
