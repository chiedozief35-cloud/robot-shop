import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def configure_tracing(app):
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT")
    if not endpoint:
        return

    provider = TracerProvider(
        resource=Resource.create({
            "service.name": os.getenv("OTEL_SERVICE_NAME", "payment"),
            "service.namespace": "robot-shop",
        })
    )
    provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(endpoint=endpoint, timeout=5),
            max_queue_size=256,
            max_export_batch_size=64,
            schedule_delay_millis=1000,
        )
    )
    trace.set_tracer_provider(provider)

    FlaskInstrumentor().instrument_app(
        app,
        excluded_urls=r".*/(metrics|health)(\?.*)?$",
    )
    RequestsInstrumentor().instrument()
