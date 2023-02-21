from pymccool.logging import Logger, LoggerKwargs
from contextlib import redirect_stdout
import io


def test_logger():
    """
    Basic check of logging functionality to stream logger (assumed file handlers are similar)
    Check that by default, stream logging level is INFO, and that the log level is included in the printed line.
    """
    s = io.StringIO()
    with redirect_stdout(s):
        logger = Logger(app_name="test_logger")
        logger.verbose(
            "Test Verbose"
        )    # Verbose is below the default threshold, will not be printed
        logger.info("Test Info")
        logger.debug(
            "Test Debug"
        )    # Debug is below the default threshold, will not be printegit
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
    s = io.StringIO()
    with redirect_stdout(s):
        logger = Logger(app_name="test_logger_verbose",
                        default_level=Logger.VERBOSE,
                        stream_level=Logger.VERBOSE)
        logger.verbose("Test Verbose")

    handlers = logger._logger.handlers
    assert len(handlers) == 3
    assert logger._logger.level == logger.VERBOSE
    assert logger._logger.isEnabledFor(logger.VERBOSE)

    logged_lines = s.getvalue().strip("\n").split("\n")
    assert len(logged_lines) == 1
    assert "VERBOSE-1" in logged_lines[0]
    assert "Test Verbose" in logged_lines[0]

    logger.close()


def test_logger_verbose_protocol():
    s = io.StringIO()
    with redirect_stdout(s):
        logger = Logger(
            LoggerKwargs(app_name="test_logger_verbose",
                         default_level=Logger.VERBOSE,
                         stream_level=Logger.VERBOSE))
        logger.verbose("Test Verbose")

    handlers = logger._logger.handlers
    assert len(handlers) == 3
    assert logger._logger.level == logger.VERBOSE
    assert logger._logger.isEnabledFor(logger.VERBOSE)

    logged_lines = s.getvalue().strip("\n").split("\n")
    assert len(logged_lines) == 1
    assert "VERBOSE-1" in logged_lines[0]
    assert "Test Verbose" in logged_lines[0]

    logger.close()


def test_logger_pprint():
    s = io.StringIO()
    with redirect_stdout(s):
        a = {
            "TODO": ["Don't Change Your Number"],
            "Name": "Jenny",
            "Number": 8675309,
            "Numbers":
            ["Eight", "Six", "Seven", "Five", "Three", "Oh", "Nine"]
        }
        logger = Logger(app_name="test_logger", stream_color=False)
        logger.pretty(Logger.INFO, a)

    logged_lines = s.getvalue().strip("\n").split("\n")
    assert len(logged_lines) == 4

    line_no = 0
    assert "INFO" in logged_lines[line_no]
    assert "test_logger.test_logger.test_logger_pprint" in logged_lines[
        line_no]
    assert "'Name': 'Jenny'" in logged_lines[line_no]

    line_no += 1
    assert "INFO" in logged_lines[line_no]
    assert "test_logger.test_logger.test_logger_pprint" in logged_lines[
        line_no]
    assert "'Number': 8675309," in logged_lines[line_no]

    line_no += 1
    assert "INFO" in logged_lines[line_no]
    assert "test_logger.test_logger.test_logger_pprint" in logged_lines[
        line_no]
    assert "'Numbers': ['Eight', 'Six', 'Seven', 'Five', 'Three', 'Oh', 'Nine']," in logged_lines[
        line_no]

    line_no += 1
    assert "INFO" in logged_lines[line_no]
    assert "test_logger.test_logger.test_logger_pprint" in logged_lines[
        line_no]
    assert "'TODO': [\"Don't Change Your Number\"]}" in logged_lines[line_no]

    logger.close()


def test_multiple_instantion():
    s = io.StringIO()
    with redirect_stdout(s):
        logger = Logger(app_name="test_logger")
        logger = Logger(app_name="test_logger")
        logger = Logger(app_name="test_logger")
        logger.verbose(
            "Test Verbose"
        )    # Verbose is below the default threshold, will not be printed
        logger.info("Test Info")
        logger.debug(
            "Test Debug"
        )    # Debug is below the default threshold, will not be printed
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


def test_logger_loki():
    """
    Basic check of logging functionality to stream logger (assumed file handlers are similar)
    Check that by default, stream logging level is INFO, and that the log level is included in the printed line.
    """
    s = io.StringIO()
    with redirect_stdout(s):
        logger = Logger(
            LoggerKwargs(
                app_name="test_logger_loki",
                default_level=Logger.VERBOSE,
                stream_level=Logger.VERBOSE,
                grafana_loki_endpoint="http://127.0.0.1:3100/loki/api/v1/push")
        )
        logger.verbose("Test Verbose")
        logger.info("Test Info")
        logger.debug("Test Debug")
        logger.warning("Test Warning")
        logger.critical("Test Critical")
        logger.error("Test Error")

    handlers = logger._logger.handlers
    assert len(handlers) == 4

    logged_lines = s.getvalue().strip("\n").split("\n")
    assert len(logged_lines) == 6
    assert "VERBOSE-1" in logged_lines[0]
    assert "Test Verbose" in logged_lines[0]
    assert "INFO" in logged_lines[1]
    assert "Test Info" in logged_lines[1]
    assert "DEBUG" in logged_lines[2]
    assert "Test Debug" in logged_lines[2]
    assert "WARNING" in logged_lines[3]
    assert "Test Warning" in logged_lines[3]
    assert "CRITICAL" in logged_lines[4]
    assert "Test Critical" in logged_lines[4]
    assert "ERROR" in logged_lines[5]
    assert "Test Error" in logged_lines[5]

    logger.close()
