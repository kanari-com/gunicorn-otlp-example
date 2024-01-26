from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
    OTLPMetricExporter,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

    resource = Resource.create(attributes={
        "service.name": "api-service"
    })

    trace.set_tracer_provider(TracerProvider(resource=resource))
    span_processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint="http://localhost:14499/otlp/v1/traces")
    )
    trace.get_tracer_provider().add_span_processor(span_processor)

    reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(
            endpoint="https://<DYNATRACE_ENV>/api/v2/otlp/v1/metrics",
            headers={'Authorization': 'Api-Token <DYNATRACE_TOKEN>'}
            )
    )
    metrics.set_meter_provider(
        MeterProvider(
            resource=resource,
            metric_readers=[reader],
        )
    )