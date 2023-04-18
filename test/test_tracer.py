""" Tests for tracer """
from datetime import datetime, timedelta
import time
import mock
from uuid import uuid1
import pytest
from pymccool.tracing import get_tracer, get_decorator



uuid = uuid1()
try:
    tracer = get_tracer(service_name="test_tracer",
                        endpoint="https://otel-rec.capricorn.brendonmccool.com/v1/traces",
                        uuid=uuid)
except: #TODO too wide
    tracer = get_tracer(service_name="test_tracer",
                    endpoint="https://otel-rec.capricorn.brendonmccool.com/v1/traces",
                    uuid=uuid,
                    otlp=False)
    
instrument = get_decorator(tracer)

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
    time.sleep(0.01)

@instrument
def func_d(*args, **kwargs):
    func_c()
    func_c()


@pytest.mark.e2e
def test_tracer():
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
    #nanos = time.replace(tzinfo=timezone.utc).timestamp()*10**9
    nanos = dtime.timestamp()*10**9
    return int(nanos)

@pytest.mark.e2e
def test_tracer_custom_time():
    
    start_time = datetime.now()# - timedelta(hours=12)
    #start_time = time.time_ns() - (1000 * 1000 * 1000 * 60 * 30)
    with tracer.start_as_current_span(name="CustomTimeSpan", start_time=datetime2ns(start_time), end_on_exit=False) as span:

        
        time.sleep(1)
        span.end(end_time=datetime2ns(start_time + timedelta(minutes=30)))


@instrument
def stackable_function(recursions: int, sleep_time_s: float):
    time.sleep(sleep_time_s)
    if recursions > 0:
        recursions = recursions - 1
        stackable_function(recursions=recursions, sleep_time_s=sleep_time_s)

@pytest.mark.e2e
def test_tracer_stacking():
    stackable_function(5, 0.01)

