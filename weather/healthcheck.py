#!/bin/python3
"""
Script to periodically test:
    - API connectivity.
    - DB connection.
"""

"""
#!/bin/bash

datetime=$(date --rfc-3339=s)
touch /weather/log/startup.log

# Check valid api
API=$(curl -Is --request GET \
--url 'https://yahoo-weather5.p.rapidapi.com/weather?lat=37.372&long=-122.038&format=json&u=f' \
--header 'x-rapidapi-host: yahoo-weather5.p.rapidapi.com' \
--header 'x-rapidapi-key: ' \
| head -n 1|cut -d$' ' -f2)
if [ $API -ne 200 ]; then
  echo "$datetime - ERROR - Weather API failed, status code: $API" >> /weather/log/startup.log
  exit 1
else
  echo "$datetime - INFO - Weather API valid, status code: $API" >> /weather/log/startup.log
fi
"""