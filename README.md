# influx db
*(in progress...)*
Developing basic applications to generate time-series data, ingest it into influx db, then build Grafana dashboards from influx db tables (measurements).

---

## Usage
Stuff I need frequently during development...

Test port binding with vagrant developent box
`curl -G http://localhost:8086/query --data-urlencode "q=SHOW DATABASES" | jq`

Ping db:
`curl -sl -I localhost:8086/ping`
Example response:
```buildoutcfg
HTTP/1.1 204 No Content
Content-Type: application/json
Request-Id: 2025c3b0-fcb2-11eb-8006-0242ac110002
X-Influxdb-Build: OSS
X-Influxdb-Version: 1.8.9
X-Request-Id: 2025c3b0-fcb2-11eb-8006-0242ac110002
Date: Sat, 14 Aug 2021 03:45:53 GMT
```

HTTP 204 implies your InfluxDB instance is up and running.

Vagrantfile port forwarding
```
config.vm.network "forwarded_port", guest: 8086, host: 8086
```

Influxdb Api reference
https://archive.docs.influxdata.com/influxdb/v1.2/tools/api/

DB init:
```buildoutcfg
def init(db_name, db_client):
    """Initialization: create a database only if it doesn't exist"""
    dbs = db_client.get_list_database()
    databases = {k for d in dbs for k in d.values()}
    if db_name not in databases:
        db_client.create_database(db_name)
        print(f"DB {db_name} created successfully.")
    else:
        print(f"DB already exist.")
```

Jobs scheduling
https://github.com/dbader/schedule
https://github.com/taichino/croniter