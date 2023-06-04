FROM python:3-alpine3.15

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 5050

ENTRYPOINT ["./docker-enterypoint.sh"]