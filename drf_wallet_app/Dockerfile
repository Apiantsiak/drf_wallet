FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

COPY ./app /app
COPY ./requirements.txt requirements.txt
COPY ./entrypoint.sh /entrypoint.sh


RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
  gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

WORKDIR /app

RUN mkdir -p /vol/drf_wallet_app
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/drf_wallet_app

USER user

ENTRYPOINT [ "sh", "/entrypoint.sh" ]
