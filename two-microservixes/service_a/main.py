import time
from fastapi import FastAPI
import requests

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor


resource = Resource(
    attributes={
        "service.name": "AFE",
        "os-version": 1234.56,
        "cluster": "AFE",
        "datacentre": "BNE",
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

SERVICE_B_URL = 'http://service_b:8000'

@app.get('/')
def read_root():
    return {"message": "Service A is runnning"}

@app.get('/fetch-data')
def fetch_data():
    try:        
        response = requests.get(f"{SERVICE_B_URL}/data")
        return {"data from service_a" : response.json()}
    except Exception as e:
        return {"error": str(e)}
    

@app.post("/add")
def do_addition(first, second):
    return add_new(first, second)

@tracer.start_as_current_span("add_new")
def add_new(first, second):
    current_span = trace.get_current_span()

    # Assume a call to a feature flag backend
    feature_flag_key = "is_feature_enabled"
    flag_value = True

    if feature_flag_key == "is_feature_enabled" and flag_value:
        time.sleep(2)

    current_span.set_attributes(
        {
            SpanAttributes.FEATURE_FLAG_PROVIDER_NAME: "MyFakeFeatureFlagBackend",
            SpanAttributes.FEATURE_FLAG_KEY: feature_flag_key,
            SpanAttributes.FEATURE_FLAG_VARIANT: flag_value,
        }
    )
    return first + second

@app.post("/divide")
def do_addition(nominator, denominator):
    try:
        return_val = int(nominator) / int(denominator)    
        return {"return value is" : return_val}
    except Exception as e:
        current_span = trace.get_current_span()
        current_span.record_exception(e)
        current_span.set_status(trace.StatusCode.ERROR, str(e))
        return {"return value is" : str(e)}
    
    
@app.get("/divide-err")
def do_addition():
    return_val = int(1) / int(0)    
    return {"return value is" : return_val}

    
@app.get("/error")
def get_error():
    return {"response" : requests.get(f"{SERVICE_B_URL}/error").json()}

@app.get("/context-propagation")
def get_ctx_propagation():
    with tracer.start_as_current_span("root_task") as span:
        child_of_root()

def child_of_root():
    with tracer.start_as_current_span("child_of_root") as span:
        grandchild_of_root()

def grandchild_of_root():
    with tracer.start_as_current_span("grandchild_of_root") as span:
        return {"Hi From" : "Grandchild"}