FROM python:3.6.6

ENV PYTHONUNBUFFERED 1

RUN groupadd -r flask \
    && useradd -r -g flask flask

# Requirements are installed here to ensure they will be cached.
# Installing from intermediate in order to obfuscate PIP_EXTRA_INDEX_URL
COPY ./requirements /requirements

RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./deploy/gunicorn_config.py /gunicorn_config.py
COPY ./deploy/gunicorn_logging.conf /gunicorn_logging.conf

COPY ./deploy/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh
RUN chown flask /start.sh

COPY . /app

USER flask

WORKDIR /app

CMD ["/start.sh"]
