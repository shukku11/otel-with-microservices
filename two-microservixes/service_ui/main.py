import json
import time
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader

import requests

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from fastapi.middleware.cors import CORSMiddleware

from token_helper import get_jwt_claims
from tracing_utility import init_otel

tracer = init_otel()

RequestsInstrumentor().instrument()

app = FastAPI()

# Instrument FastAPI
FastAPIInstrumentor().instrument_app(app)

SERVICE_A_URL = "http://service_a:8001"
SERVICE_B_URL = "http://service_b:8000"

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
def read_root():
    return {"message": "Service UI is runnning"}


@app.get("/context-propagation")
def fetch_data(token_data: dict = Depends(get_jwt_claims)):
    try:
        json_data = json.dumps(token_data, indent=4)
        with tracer.start_as_current_span("process_request") as span:
            span.set_attribute("user_id", token_data["jwt_payload"]["user_id"])
            span.set_attribute("tenant_id", token_data["jwt_payload"]["tenant_id"])
            response = requests.get(f"{SERVICE_A_URL}/fetch-data")
            return {"response": response.json(), "token_data": token_data}
    except Exception as e:
        return {"error": str(e)}


@app.get("/context-propagation-two")
def fetch_data_two(token_data: dict = Depends(get_jwt_claims)):
    try:
        json_data = json.dumps(token_data, indent=4)
        with tracer.start_as_current_span("process_request") as span:
            span.set_attribute("user_id", token_data["jwt_payload"]["user_id"])
            span.set_attribute("tenant_id", token_data["jwt_payload"]["tenant_id"])
            response = requests.get(f"{SERVICE_B_URL}/fetch-data")
            return {"response": response.json(), "token_data": token_data}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/error-one")
def fetch_data_two():
     response = requests.get(f"{SERVICE_A_URL}/divide-err")
     return {"response": response.json()}
    
@app.get("/error-two")
def fetch_data_two(token_data: dict = Depends(get_jwt_claims)):
    try:
        json_data = json.dumps(token_data, indent=4)
        with tracer.start_as_current_span("process_request") as span:
            span.set_attribute("user_id", token_data["jwt_payload"]["user_id"])
            span.set_attribute("tenant_id", token_data["jwt_payload"]["tenant_id"])
            response = requests.get(f"{SERVICE_B_URL}/fetch-data1")
            return {"response": response.json(), "token_data": token_data}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/delay-simulate")
def fetch_data_two(token_data: dict = Depends(get_jwt_claims)):
    try:
        json_data = json.dumps(token_data, indent=4)
        with tracer.start_as_current_span("process_request") as span:
            span.set_attribute("user_id", token_data["jwt_payload"]["user_id"])
            span.set_attribute("tenant_id", token_data["jwt_payload"]["tenant_id"])
            time.sleep(.5)
            response = requests.get(f"{SERVICE_B_URL}/delay-simulate")
            return {"response": response.json(), "token_data": token_data}
    except Exception as e:
        return {"error": str(e)}