""" Toplevel Conftest for pytest """
import io
from contextlib import redirect_stdout
from uuid import uuid1
import pytest
from opentelemetry.trace import Tracer
from e2e_setup import OTEL_ENDPOINT, LOKI_ENDPOINT, OTEL_USERNAME, OTEL_TOKEN

from pymccool.tracing import get_tracer, get_decorator, OpenTelemetryCredentials
from pymccool.logging import Logger, LoggerKwargs

UUID = uuid1()

@pytest.fixture(scope="session")
def e2e_instrument(e2e_tracer):
    """
    Returns an instrument decorator that will send traces to the e2e test environment
    """
    instrument = get_decorator(e2e_tracer)
    yield instrument

@pytest.fixture(scope="session")
def e2e_tracer() -> Tracer:
    """
    Returns an tracer that will send traces to the e2e test environment
    """
    credentials = OpenTelemetryCredentials(username=OTEL_USERNAME,
                                             token=OTEL_TOKEN,
                                             endpoint=OTEL_ENDPOINT)
    tracer = get_tracer(service_name="test_tracer",
                        endpoint=credentials.traces_endpoint,
                        uuid=UUID,
                        headers={"authorization": f"Basic {credentials.api_encoded_token}"})
    yield tracer

@pytest.fixture(scope="session")
def e2e_logger():
    """
    Create and return a logger setup with local external loki logger
    """
    string_capture = io.StringIO()
    with redirect_stdout(string_capture):
        logger = Logger(
            LoggerKwargs(
                app_name="test_logger_loki",
                default_level=Logger.VERBOSE,
                stream_level=Logger.VERBOSE,
                grafana_loki_endpoint=LOKI_ENDPOINT,
                uuid=UUID)
        )
    yield logger
    logger.close()
