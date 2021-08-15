#!/bin/python3
import json
from src.weather.weather_data import weather_data
"""
test api
"""

import schedule
import time

"""
Script to run at container startup to schedule main.py execution time.
"""


def job(user, password):
    print(f"I'm working...{user} {password}")


schedule.every(3).seconds.do(job, user='foo', password='bar')

while True:
    schedule.run_pending()
