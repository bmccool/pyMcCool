"""Test module for verifying logger functionality"""
from contextlib import redirect_stdout
import io
import mock
import pytest
from pymccool.logging import Logger, LoggerKwargs
from logging import LogRecord
from e2e_setup import LOKI_ENDPOINT


@pytest.fixture(autouse=True, scope="module")
def session_fixture():
    logger = Logger(app_name="test_logger_loki")
    logger.close()
    yield

def test_logger():
    """
    Basic check of logging functionality to stream logger (assumed file handlers are similar)
    Check that by default, stream logging level is INFO, and that the log level is included
    in the printed line.
    """
    string_capture = io.StringIO()
    with redirect_stdout(string_capture):
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

    logged_lines = string_capture.getvalue().strip("\n").split("\n")
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
    string_capture = io.StringIO()
    with redirect_stdout(string_capture):
        logger = Logger(app_name="test_logger_verbose",
                        default_level=Logger.VERBOSE,
                        stream_level=Logger.VERBOSE)
        logger.verbose("Test Verbose")

    handlers = logger._logger.handlers
    assert len(handlers) == 3
    assert logger._logger.level == logger.VERBOSE
    assert logger._logger.isEnabledFor(logger.VERBOSE)

    logged_lines = string_capture.getvalue().strip("\n").split("\n")
    assert len(logged_lines) == 1
    assert "VERBOSE-1" in logged_lines[0]
    assert "Test Verbose" in logged_lines[0]

    logger.close()


def test_logger_verbose_protocol():
    string_capture = io.StringIO()
    with redirect_stdout(string_capture):
        logger = Logger(
            LoggerKwargs(app_name="test_logger_verbose",
                         default_level=Logger.VERBOSE,
                         stream_level=Logger.VERBOSE))
        logger.verbose("Test Verbose")

    handlers = logger._logger.handlers
    assert len(handlers) == 3
    assert logger._logger.level == logger.VERBOSE
    assert logger._logger.isEnabledFor(logger.VERBOSE)

    logged_lines = string_capture.getvalue().strip("\n").split("\n")
    assert len(logged_lines) == 1
    assert "VERBOSE-1" in logged_lines[0]
    assert "Test Verbose" in logged_lines[0]

    logger.close()


def test_logger_pprint():
    string_capture = io.StringIO()
    with redirect_stdout(string_capture):
        a = {
            "TODO": ["Don't Change Your Number"],
            "Name": "Jenny",
            "Number": 8675309,
            "Numbers":
            ["Eight", "Six", "Seven", "Five", "Three", "Oh", "Nine"]
        }
        logger = Logger(app_name="test_logger", stream_color=False)
        logger.pretty(Logger.INFO, a)

    logged_lines = string_capture.getvalue().strip("\n").split("\n")
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
    string_capture = io.StringIO()
    with redirect_stdout(string_capture):
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

    logged_lines = string_capture.getvalue().strip("\n").split("\n")
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

@pytest.mark.e2e
def test_logger_loki_e2e():
    """
    Basic check of logging functionality to stream logger (assumed file handlers are similar)
    Check that by default, stream logging level is INFO, and that the log level is included in the printed line.
    """
    string_capture = io.StringIO()
    with redirect_stdout(string_capture):
        logger = Logger(
            LoggerKwargs(
                app_name="test_logger_loki",
                default_level=Logger.VERBOSE,
                stream_level=Logger.VERBOSE,
                grafana_loki_endpoint=LOKI_ENDPOINT)
        )
        logger.verbose("Test Verbose")
        logger.info("Test Info")
        logger.debug("Test Debug")
        logger.warning("Test Warning")
        logger.critical("Test Critical")
        logger.error("Test Error")

    handlers = logger._logger.handlers
    assert len(handlers) == 4

    logged_lines = string_capture.getvalue().strip("\n").split("\n")
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

def test_logger_loki_unit():
    """
    Basic check of logging functionality to stream logger (assumed file handlers are similar)
    Check that by default, stream logging level is INFO, and that the log level is included in the printed line.
    """
    string_capture = io.StringIO()
    with redirect_stdout(string_capture):
        logger2 = Logger(
            LoggerKwargs(
                app_name="test_logger_loki",
                default_level=Logger.VERBOSE,
                stream_level=Logger.VERBOSE,
                grafana_loki_endpoint="https://loki.fake.endpoint.com/loki/api/v1/push")
        )

    with mock.patch("logging_loki.handlers.LokiHandler.emit") as loki_emit:
        logger2.verbose("Test Verbose")
        logger2.info("Test Info")
        logger2.debug("Test Debug")
        logger2.warning("Test Warning")
        logger2.critical("Test Critical")
        logger2.error("Test Error")

        assert loki_emit.call_count == 6
        assert loki_emit.call_args_list[0][0][0].name == "test_logger_loki"
        assert loki_emit.call_args_list[0][0][0].levelno == 5
        assert loki_emit.call_args_list[0][0][0].levelname == "VERBOSE-1"
        assert loki_emit.call_args_list[0][0][0].msg == "Test Verbose"
        
        assert loki_emit.call_args_list[1][0][0].name == "test_logger_loki"
        assert loki_emit.call_args_list[1][0][0].levelno == 20
        assert loki_emit.call_args_list[1][0][0].levelname == "INFO"
        assert loki_emit.call_args_list[1][0][0].msg == "Test Info"

        assert loki_emit.call_args_list[2][0][0].name == "test_logger_loki"
        assert loki_emit.call_args_list[2][0][0].levelno == 10
        assert loki_emit.call_args_list[2][0][0].levelname == "DEBUG"
        assert loki_emit.call_args_list[2][0][0].msg == "Test Debug"

        assert loki_emit.call_args_list[3][0][0].name == "test_logger_loki"
        assert loki_emit.call_args_list[3][0][0].levelno == 30
        assert loki_emit.call_args_list[3][0][0].levelname == "WARNING"
        assert loki_emit.call_args_list[3][0][0].msg == "Test Warning"

        assert loki_emit.call_args_list[4][0][0].name == "test_logger_loki"
        assert loki_emit.call_args_list[4][0][0].levelno == 50
        assert loki_emit.call_args_list[4][0][0].levelname == "CRITICAL"
        assert loki_emit.call_args_list[4][0][0].msg == "Test Critical"

        assert loki_emit.call_args_list[5][0][0].name == "test_logger_loki"
        assert loki_emit.call_args_list[5][0][0].levelno == 40
        assert loki_emit.call_args_list[5][0][0].levelname == "ERROR"
        assert loki_emit.call_args_list[5][0][0].msg == "Test Error"

    handlers = logger2._logger.handlers
    assert len(handlers) == 4

    logged_lines = string_capture.getvalue().strip("\n").split("\n")
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

    logger2.close()

def test_issue_14():
    """
    Basic check of logging functionality to stream logger (assumed file handlers are similar)
    Check that by default, stream logging level is INFO, and that the log level is included
    in the printed line.
    """
    string_capture = io.StringIO()
    with redirect_stdout(string_capture):
        logger = Logger(app_name="test_logger")
        logger.info("Test Info", end="")
        logger.info("- Test Info")

    logged_lines = string_capture.getvalue().strip("\n").split("\n")
    assert len(logged_lines) == 1
    assert "INFO" in logged_lines[0]
    assert "Test Info" in logged_lines[0]


    logger.close()