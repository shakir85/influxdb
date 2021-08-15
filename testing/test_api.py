#!/bin/python3
"""
test api
"""

import schedule

"""
Script to run at container startup to schedule main.py execution time.
"""


def job(user, password):
    print(f"I'm working...{user} {password}")


schedule.every(3).seconds.do(job, user='foo', password='bar')

while True:
    schedule.run_pending()
