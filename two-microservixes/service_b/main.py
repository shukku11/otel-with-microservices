import time
from fastapi import FastAPI, HTTPException

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import requests
from opentelemetry.instrumentation.requests import RequestsInstrumentor

resource = Resource(
    attributes={
        "service.name": "Model Server",
        "os-version": 1234.56,
        "cluster": "Model Server",
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

RequestsInstrumentor().instrument()

app = FastAPI()

# Instrument FastAPI
FastAPIInstrumentor().instrument_app(app)

SERVICE_C_URL = 'http://service_c:8003'

@app.get('/')
def read_root():
    time.sleep(1)
    return {"message": "Service B is runnning"}

@app.get('/data')
def data():
    return {"Service B is running"}

@app.get('/error')
def error():
    raise HTTPException(status_code=400, detail="Throw an exception")

@app.get('/fetch-data')
def fetch_data():
    try:        
        response = requests.get(f"{SERVICE_C_URL}/data")
        return {"data from service_b" : response.json()}
    except Exception as e:
        return {"error": str(e)}

@app.get('/delay-simulate')
def fetch_data():
    try:        
        time.sleep(2)
        response = requests.get(f"{SERVICE_C_URL}/delay-simulate")
        return {"data from service_b" : response.json()}
    except Exception as e:
        return {"error": str(e)}