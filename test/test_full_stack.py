""" Tests for logging/tracing combined """
#import random
#import pytest
#from pymccool.logging import Logger


#@pytest.fixture(autouse=True, scope="module")
#def session_fixture(e2e_instrument):
#    """
#    Provide a fixture to handle setup/teardown for the module
#    Note 1: Because the instrument decorator relies on external services 
#    which may not be availble, we decorate "manually" inside this session
#    fixture, which garuntees the tests have been marked for execution.
#    """
#    global set_test_point
#    global verify_properties
#    instrument = e2e_instrument
#    set_test_point = instrument(set_test_point)
#    verify_properties = instrument(verify_properties)
#    yield
#
#
##@instrument See Note 1
#def set_test_point(temperature: int, voltage: int, logger: Logger) -> None:
#    logger.info(f"Setting test point to {temperature}C, {voltage}mV")
#    while not bool(random.getrandbits(1)):
#        logger.debug("Still waiting for DUT to report correct test point...")
#    logger.info("Test point set!")
#    
##@instrument See Note 1
#def verify_properties(temperature: int, voltage: int, logger: Logger) -> None:
#    logger.info("Verifying region properties")
#    set_test_point(temperature=temperature, voltage=voltage, logger=logger)
#
#@pytest.mark.e2e
#def test_region_properties(e2e_logger):
#    """
#    Demo for full stack test
#    """
#    verify_properties(temperature=30, voltage=4000, logger=e2e_logger)
#