from pym.logging import Logger
from contextlib import redirect_stdout
import io

def test_logger():
    print()
    s = io.StringIO()
    with redirect_stdout(s):
        logger = Logger(app_name="test_logger")
        logger.verbose("Test Verbose") # Verbose is below the default threshold, will not be printed
        logger.info("Test Info")
        logger.debug("Test Debug") # Debug is below the default threshold, will not be printed
        logger.warning("Test Warning")
        logger.critical("Test Critical")
        logger.error("Test Error")

    logged_lines = s.getvalue().strip("\n").split("\n")
    assert len(logged_lines) == 4
    assert "INFO" in logged_lines[0]
    assert "Test Info" in logged_lines[0]
    assert "WARNING" in logged_lines[1]
    assert "Test Warning" in logged_lines[1]
    assert "CRITICAL" in logged_lines[2]
    assert "Test Critical" in logged_lines[2]
    assert "ERROR" in logged_lines[3]
    assert "Test Error" in logged_lines[3]

    logger.close()

def test_logger_verbose():
    print()
    s = io.StringIO()
    with redirect_stdout(s):
        logger = Logger(app_name="test_logger_verbose", default_level=Logger.VERBOSE, stream_level=Logger.VERBOSE)
        logger.verbose("Test Verbose")


    handlers = logger._logger.handlers
    assert len(handlers) == 3
    assert logger._logger.level == logger.VERBOSE
    assert logger._logger.isEnabledFor(logger.VERBOSE)

    for handler in handlers: print(handler)

    logged_lines = s.getvalue().strip("\n").split("\n")
    assert len(logged_lines) == 1
    assert "VERBOSE-1" in logged_lines[0]
    assert "Test Verbose" in logged_lines[0]


