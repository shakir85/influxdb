FROM python:3.8-buster

RUN mkdir -p /weather/conf && mkdir /weather/app

ENV APP_USER    appuser
ENV APP_GROUP   appgroup

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y -q --no-install-recommends curl htop vim && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 9999 ${APP_GROUP} &&  useradd -g 9999 -d /weather -s /bin/bash ${APP_USER}

COPY utilities/ /weather/conf
COPY weather_data.py /weather/app
COPY main.py /weather/app
COPY requirements.txt /weather

RUN chown -R $APP_USER:$APP_GROUP /weather/
RUN chmod -R 750 /weather/
USER $APP_USER

WORKDIR /weather

RUN pip3 install -r requirements.txt virtualenv

ENV PYTHONPATH=/weather

EXPOSE 8086

#CMD echo "" && sleep 3600
CMD python app/main.py -u -p -k
