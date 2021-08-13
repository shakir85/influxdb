# influx db

Developing basic applications to generate time-series data and ingest it into influx db. Then generate Grafana dashboards from influx db tables (measurements).

---

Test port binding with vagrant developent box
`curl -G http://localhost:8086/query --data-urlencode "q=SHOW DATABASES" | jq`

Vagrantfile
```
config.vm.network "forwarded_port", guest: 8086, host: 8086
```