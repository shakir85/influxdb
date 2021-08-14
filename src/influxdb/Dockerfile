FROM influxdb:1.8.9

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y --no-install-recommends htop vim && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN rm -rf /etc/influxdb/influxdb.conf
COPY ./influxdb.conf /etc/influxdb

EXPOSE 8086