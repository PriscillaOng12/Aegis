from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter


def setup_tracing(app: FastAPI) -> None:
    """Configure OpenTelemetry tracing for the FastAPI app."""
    resource = Resource(attributes={SERVICE_NAME: "aegis-api"})
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter()
    span_processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor().instrument_app(app, tracer_provider=provider)