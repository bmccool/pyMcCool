from pymccool.logging import Logger
from contextlib import redirect_stdout
import io
import pprint

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



def test_logger_pprint():
    print()
    s = io.StringIO()
    with redirect_stdout(s):
        a = {"TODO": ["Don't Change Your Number"], "Name": "Jenny", "Number": 8675309, "Numbers": ["Eight", "Six", "Seven", "Five", "Three", "Oh", "Nine"]}
        logger = Logger(app_name="test_logger", stream_color=False)
        logger.pretty(Logger.INFO, a)

    logged_lines = s.getvalue().strip("\n").split("\n")
    assert len(logged_lines) == 4
    
    line_no = 0
    assert "INFO" in logged_lines[line_no]
    assert "test_logger.test_logger.test_logger_pprint" in logged_lines[line_no]
    assert "'Name': 'Jenny'" in logged_lines[line_no]

    line_no += 1
    assert "INFO" in logged_lines[line_no]
    assert "test_logger.test_logger.test_logger_pprint" in logged_lines[line_no]
    assert "'Number': 8675309," in logged_lines[line_no]

    line_no += 1
    assert "INFO" in logged_lines[line_no]
    assert "test_logger.test_logger.test_logger_pprint" in logged_lines[line_no]
    assert "'Numbers': ['Eight', 'Six', 'Seven', 'Five', 'Three', 'Oh', 'Nine']," in logged_lines[line_no]

    line_no += 1
    assert "INFO" in logged_lines[line_no]
    assert "test_logger.test_logger.test_logger_pprint" in logged_lines[line_no]
    assert "'TODO': [\"Don't Change Your Number\"]}" in logged_lines[line_no]