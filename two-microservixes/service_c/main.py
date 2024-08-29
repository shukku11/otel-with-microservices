import time
from fastapi import FastAPI, HTTPException

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

resource = Resource(
    attributes={
        "service.name": "GenAI Inference",
        "os-version": 1234.56,
        "cluster": "GenAI Inference",
        "datacentre": "XYZ",
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

app = FastAPI()

# Instrument FastAPI
FastAPIInstrumentor().instrument_app(app)

@app.get('/')
def read_root():
    time.sleep(1)
    return {"message": "Service Gen AI  is runnning"}

@app.get('/data')
def data():
    return {"Service Gen AI is running"}

@app.get('/delay-simulate')
def data():
    call_to_db()
    return {"Service Gen AI is running"}

@app.get('/error')
def error_data():
    raise HTTPException(status_code=400, detail="Throw an exception")

def call_to_db():
    time.sleep(1)