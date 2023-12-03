""" Tests for tracer """
from datetime import datetime, timedelta
import time
import mock
import pytest
from opentelemetry.trace import Tracer

def func_a(*args, **kwargs):
    func_b()
    func_b()

def func_b(*args, **kwargs):
    func_c()
    func_c()
    func_d()
    func_c()

def func_c(*args, **kwargs):
    time.sleep(0.01)

def func_d(*args, **kwargs):
    func_c()
    func_c()

@pytest.mark.e2e
def test_tracer(tracer_e2e_fixture):
    """
    Basic tracer test
    """
    func_a()

def test_tracer_unit():
    """
    Basic tracer test with mocked calls
    """
    with mock.patch("opentelemetry.trace.Tracer.start_as_current_span") as start_as_current_span:
        with mock.patch("opentelemetry.trace.span.Span.set_attribute") as set_attribute:
            func_a()


def datetime2ns(dtime: datetime) -> int:
    nanos = dtime.timestamp()*10**9
    return int(nanos)

@pytest.mark.e2e
def test_tracer_custom_time(e2e_tracer, tracer_e2e_fixture):
    tracer: Tracer = e2e_tracer
    start_time = datetime.now()# - timedelta(hours=12)
    with tracer.start_as_current_span(name="CustomTimeSpan", start_time=datetime2ns(start_time), end_on_exit=False) as span:
        time.sleep(1)
        span.end(end_time=datetime2ns(start_time + timedelta(minutes=30)))


def stackable_function(recursions: int, sleep_time_s: float):
    time.sleep(sleep_time_s)
    if recursions > 0:
        recursions = recursions - 1
        stackable_function(recursions=recursions, sleep_time_s=sleep_time_s)

@pytest.mark.e2e
def test_tracer_stacking(tracer_e2e_fixture):
    stackable_function(5, 0.01)

@pytest.fixture(scope="module")
def tracer_e2e_fixture(e2e_instrument):
    """
    Provide a fixture to handle setup/teardown for the module
    Note 1: Because the instrument decorator relies on external services 
    which may not be availble, we decorate "manually" inside this session
    fixture, which garuntees the tests have been marked for execution.
    """
    global func_a
    global func_b
    global func_c
    global func_d
    global stackable_function
    instrument = e2e_instrument
    func_a = instrument(func_a)
    func_b = instrument(func_b)
    func_c = instrument(func_c)
    func_d = instrument(func_d)
    stackable_function = instrument(stackable_function)
    yield