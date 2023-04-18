""" Tests for logging/tracing combined """
from contextlib import redirect_stdout
import io
from uuid import uuid1
import time
import random
import pytest
from datetime import datetime, timedelta, timezone
from opentelemetry import trace, baggage
from pymccool.logging import Logger, LoggerKwargs
from pymccool.tracing import get_tracer, get_decorator



uuid = uuid1()
tracer = get_tracer(service_name="test_tracer",
                    endpoint="https://otel-rec.capricorn.brendonmccool.com/v1/traces",
                    uuid=uuid)
instrument = get_decorator(tracer)

string_capture = io.StringIO()
with redirect_stdout(string_capture):
    logger = Logger(
        LoggerKwargs(
            app_name="test_logger_loki",
            default_level=Logger.VERBOSE,
            stream_level=Logger.VERBOSE,
            grafana_loki_endpoint="https://loki.capricorn.brendonmccool.com/loki/api/v1/push",
            uuid=uuid)
    )

@pytest.fixture(autouse=True, scope="module")
def session_fixture():
    """
    Provide a fixture to handle setup/teardown for the module
    """
    yield
    logger.close()



@instrument
def func_a(*args, **kwargs):
    func_b()
    func_b()

@instrument
def func_b(*args, **kwargs):
    func_c()
    func_c()
    func_d()
    func_c()

@instrument
def func_c(*args, **kwargs):
    time.sleep(1)

@instrument
def func_d(*args, **kwargs):
    func_c()
    func_c()

@instrument
def set_test_point(temperature: int, voltage: int) -> None:
    logger.info(f"Setting test point to {temperature}C, {voltage}mV")
    while not bool(random.getrandbits(1)):
        logger.debug("Still waiting for DUT to report correct test point...")
    logger.info("Test point set!")
    
@instrument
def verify_properties(temperature: int, voltage: int) -> None:
    logger.info("Verifying region properties")
    set_test_point(temperature=temperature, voltage=voltage)

@pytest.mark.e2e
def test_region_properties():
    """
    Demo for full stack test
    """
    verify_properties(30, 4000)
