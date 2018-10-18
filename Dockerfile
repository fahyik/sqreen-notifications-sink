FROM python:3.6.6-alpine3.7

ARG PIP_EXTRA_INDEX_URL

RUN adduser -D flask

RUN apk update && apk add --virtual build-deps gcc libc-dev

# Requirements are installed here to ensure they will be cached.
# Installing from intermediate in order to obfuscate PIP_EXTRA_INDEX_URL
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt \
    && rm /requirements.txt

COPY ./gunicorn.sh /gunicorn.sh
RUN chmod +x /gunicorn.sh


COPY . /app

USER flask

WORKDIR /app

ENV FLASK_APP=products

ENTRYPOINT ["/gunicorn.sh"]
