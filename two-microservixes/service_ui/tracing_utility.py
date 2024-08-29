from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from fastapi.middleware.cors import CORSMiddleware

def init_otel():    
    resource = Resource(
        attributes={
            "service.name": "UI"
        }
    )
    provider = TracerProvider(resource=resource)

    COLLECTOR_ENDPOINT = "otel-collector"
    COLLECTOR_GRPC_PORT = 4317

    # processor = BatchSpanProcessor(ConsoleSpanExporter())
    processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint=f"http://{COLLECTOR_ENDPOINT}:{COLLECTOR_GRPC_PORT}",insecure=True)
    )
    provider.add_span_processor(processor)

    # Sets the global default tracer provider
    trace.set_tracer_provider(provider)

    # Creates a tracer from the global tracer provider
    tracer = trace.get_tracer("Vivek.tracer.name")
    return tracer