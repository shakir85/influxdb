FROM python:3.8-buster

## RUN apt installs
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y -q --no-install-recommends \
        curl \
        htop \
        vim \
    && rm -rf /var/lib/apt/lists/*

## RUN mkdirs
RUN mkdir -p /weather/conf \
    && mkdir /weather/app

ENV APP_USER    appuser
ENV APP_GROUP   appgroup

RUN groupadd -g 1111 ${APP_GROUP} && \
    useradd -g 1111 -d /weather -s /bin/bash ${APP_USER}

RUN chown -R $APP_USER:$APP_GROUP /weather
RUN chmod -R 750 /weather

USER $RUN_USER

COPY startup.py /weather/conf
COPY weather_data.py /weather/app
COPY main.py /weather/app
COPY requirements.txt /weather

WORKDIR /weather

RUN pip3 install -r requirements.txt virtualenv

ENV PYTHONPATH=/weather

EXPOSE 8086

#CMD echo "" && sleep 3600
CMD ["/weather/app/main.py", "-u root", "-p root", "-k"]
