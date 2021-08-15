FROM python:alpine3.13

RUN mkdir -p /weather/app && mkdir /weather/log

ENV APP_USER    appuser
ENV APP_GROUP   appgroup

RUN apk update && apk add curl htop vim

# -g is the GID
RUN addgroup -g 33445 ${APP_GROUP}

# -u is the UID
# -D permits to create an user without password
RUN adduser -u 11223 -G ${APP_GROUP} -h /weather -D ${APP_USER}

COPY db_init.py /weather/app
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

CMD python /weather/app/main.py -u  -p  -k
