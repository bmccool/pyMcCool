from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter)
import functools
from typing import Any, Callable

from opentelemetry.trace import Tracer
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from typing import Any, Callable


def get_tracer(service_name: str = "DefaultServiceName",
               endpoint: str = "localhost:4317") -> Tracer:
    # Service name is required for most backends
    resource = Resource(attributes={SERVICE_NAME: service_name})

    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint=endpoint, insecure=True))
    #processor = BatchSpanProcessor(ConsoleSpanExporter())

    provider.add_span_processor(processor)

    # Sets the global default tracer provider
    trace.set_tracer_provider(provider)

    # Creates a tracer from the global tracer provider
    tracer = trace.get_tracer(__name__)

    return tracer


def instrument_with(func: Callable[..., Any], tracer: Tracer) -> Callable[..., Any]:
    """ decorator used to create trace info for function calls """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with tracer.start_as_current_span(name=func.__qualname__) as span:
            span.set_attribute("args", str(args))
            span.set_attribute("kwargs", str(kwargs))
            return func(*args, **kwargs)
    return wrapper

def get_decorator(tracer: Tracer):
    """ Given a Tracer object, return a decorator """
    return functools.partial(instrument_with, tracer=tracer)
