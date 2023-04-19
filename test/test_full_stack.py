""" Tests for logging/tracing combined """
from contextlib import redirect_stdout
import functools
import io
from uuid import uuid1
import time
from typing import Any, Callable
import random
import pytest
from pymccool.logging import Logger, LoggerKwargs
from pymccool.tracing import get_tracer, get_decorator

def mock_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    """ Mock Decorator """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)
    return wrapper

def get_mock_decorator():
    """ Return mock tracing decorator as paceholder """
    return mock_decorator


uuid = uuid1()
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

instrument = mock_decorator

@pytest.fixture(autouse=True, scope="module")
def session_fixture():
    """
    Provide a fixture to handle setup/teardown for the module
    """
    global instrument
    global uuid
    tracer = get_tracer(service_name="test_tracer",
                        endpoint="https://otel-rec.capricorn.brendonmccool.com/v1/traces",
                        uuid=uuid)
    instrument = get_decorator(tracer)
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
