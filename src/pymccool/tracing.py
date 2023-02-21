from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter)

from opentelemetry.trace import Tracer
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


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
