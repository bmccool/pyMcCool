""" Tracing utilities for pymccool """
import functools
from typing import Any, Callable
from uuid import UUID, uuid1

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter)
from opentelemetry.trace import Tracer
#from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
import base64

class OpenTelemetryCredentials:
    def __init__(self, username, token, endpoint):
        self.username = username
        self.api_token = token
        self.api_encoded_token = base64.b64encode(
            f"{self.username}:{self.api_token}".encode("utf-8")
        ).decode("utf-8")
        self.endpoint = endpoint
        if self.endpoint:
            self.traces_endpoint = self.endpoint + "/v1/traces"
            self.metrics_endpoint = self.endpoint + "/v1/metrics"
            self.logs_endpoint = self.endpoint + "/v1/logs"

def is_configured(self):
    # Check if all the necessary variables are present
    return all([self.username, self.api_token, self.endpoint])

def get_tracer(service_name: str = "DefaultServiceName",
               endpoint: str = "localhost:4317",
               uuid: UUID = None,
               otlp: bool = True,
               headers=None,
               ) -> Tracer:
    """ Creates a tracer with the given service name """

    uuid = uuid or uuid1()

    # Service name is required for most backends
    resource = Resource(attributes={SERVICE_NAME: service_name, "UUID": str(uuid)})

    provider = TracerProvider(resource=resource)

    if otlp:
        otlp_processor = BatchSpanProcessor(
            OTLPSpanExporter(endpoint=endpoint,
                             headers=headers)
        )

    console_processor = BatchSpanProcessor(
        ConsoleSpanExporter(out=open("test_span.json", "w", encoding="utf-8")))

    if otlp:
        provider.add_span_processor(otlp_processor)
    provider.add_span_processor(console_processor)

    # Sets the global default tracer provider
    trace.set_tracer_provider(provider)

    # Creates a tracer from the global tracer provider
    tracer = trace.get_tracer(__name__)

    return tracer


def instrument_with(func: Callable[..., Any], tracer: Tracer) -> Callable[..., Any]:
    """ decorator used to create trace info for function calls """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        parent_context = trace.get_current_span().get_span_context()
        parent_link = trace.Link(parent_context)
        links = [parent_link] if parent_link.context.trace_id != 0 else None
        with tracer.start_as_current_span(name=func.__qualname__, links=links) as span:
            span.set_attribute("args", str(args))
            span.set_attribute("kwargs", str(kwargs))
            return func(*args, **kwargs)
    return wrapper

def get_decorator(tracer: Tracer):
    """ Given a Tracer object, return a decorator """
    return functools.partial(instrument_with, tracer=tracer)
