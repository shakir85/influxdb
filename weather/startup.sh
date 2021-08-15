#!/bin/bash

datetime=$(date --rfc-3339=s)
touch /weather/log/startup.log

# Check valid api
API=$(curl -Is --request GET \
--url 'https://yahoo-weather5.p.rapidapi.com/weather?lat=37.372&long=-122.038&format=json&u=f' \
--header 'x-rapidapi-host: yahoo-weather5.p.rapidapi.com' \
--header 'x-rapidapi-key: a825cc216cmshc5195bbf0afb97ep1a0afejsne4986faee612' \
| head -n 1|cut -d$' ' -f2)
if [ $API -ne 200 ]; then
  echo "$datetime - ERROR - Weather API failed, status code: $API" >> /weather/log/startup.log
  exit 1
else
  echo "$datetime - INFO - Weather API valid, status code: $API" >> /weather/log/startup.log
fi

# Start DB initialization
python  /weather/conf/db_init.py
status=$?
if [ $status -ne 0 ]; then
  echo "$datetime - ERROR - Failed to start db_init.py: $status" >> /weather/log/startup.log
  exit $status
else
  ehco "$datetime - INFO - Execution success - db_init.py: $status" >> /weather/log/startup.log
fi

# Start weather app
python /weather/app/main.py -u -p -k
status=$?
if [ $status -ne 0 ]; then
  echo "$datetime - ERROR - Failed to start main.py: $status" >> /weather/log/startup.log
  exit $status
else
  ehco "$datetime - INFO - Execution success - main.py: $status" >> /weather/log/startup.log
fi