FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install --no-cache-dir opentelemetry-distro opentelemetry-exporter-otlp opentelemetry-instrumentation-flask
COPY ./gunicorn.conf.py /code/gunicorn.conf.py
COPY ./app /code/app
EXPOSE 8000
ENV OTEL_EXPORTER_OTLP_ENDPOINT=https://<DYNATRACE ENVIRONMENT>/api/v2/otlp
ENV OTEL_EXPORTER_OTLP_HEADERS=Authorization=Api-Token%20<DYNATRACE TOKEN>
ENV OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
ENV OTEL_SERVICE_NAME="python-quickstart"
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.main:app"]
#CMD ["opentelemetry-instrument", "--traces_exporter=console", "--log_level=debug", "logs_exporter=console", "--metrics_exporter=none", "gunicorn", "--bind", "0.0.0.0:8000", "app.main:app"]
CMD opentelemetry-instrument \
    --traces_exporter console,otlp \
    --metrics_exporter console \
    gunicorn \
    --bind 0.0.0.0:8000 \
    -c gunicorn.conf.py \
    app.main:app
    