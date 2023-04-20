import functools
import io
from contextlib import redirect_stdout
from uuid import uuid1
from typing import Any, Callable
import pytest
from opentelemetry.trace import Tracer
from pymccool.tracing import get_tracer, get_decorator
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
    tracer = get_tracer(service_name="test_tracer",
                        endpoint="https://otel-rec.capricorn.brendonmccool.com/v1/traces",
                        uuid=UUID)
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
                grafana_loki_endpoint="https://loki.capricorn.brendonmccool.com/loki/api/v1/push",
                uuid=UUID)
        )
    yield logger
    logger.close()
