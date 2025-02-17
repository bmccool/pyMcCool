import logging
from logging.handlers import RotatingFileHandler
import sys
from dataclasses import dataclass
from typing import Optional
import os
import pprint

from colorlog import ColoredFormatter
from logging_loki import LokiHandler, emitter
from uuid import UUID, uuid1


@dataclass
class LoggerKwargs:
    """
    Class containing all kwargs for the Logger class

    :param app_name: Name of the application
    :param default_level: Logging level for the application
    :param stream_color: Enable or disable colors for the stream handler
    :param stream_level: Logging level for the stream handler
    :param grafana_loki_endpoint: URL for the Grafana Loki endpoint
    :param grafana_tempo_endpoint: URL for the Grafana Tempo endpoint
    :param uuid: UUID for the application instance
    """
    app_name: str = "default_logger"
    default_level: int = logging.DEBUG
    stream_color: bool = True
    stream_level: int = logging.INFO
    grafana_loki_endpoint: str = ""
    grafana_tempo_endpoint: str = ""
    base_path: str = os.path.join(os.getcwd(), "Logs")
    uuid: UUID = uuid1()


class Logger:
    """
    Opinionated logger with built in creature comforts
    """
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    VERBOSE = 5
    NOTSET = 0

    def __init__(self, config: Optional[LoggerKwargs] = None, **kwargs):
        """
        Create a logger with the given LoggerKwargs configuration.  If no configuration is provided,
        a sensible default will be used.  Or pass individual configuration options as keyword
        arguments to override the defaults.
        """
        if config is None:
            config = LoggerKwargs(**kwargs)
        self.config = config

        # Create logger based on application name
        self.app_name = config.app_name
        self._logger = logging.getLogger(self.app_name)

        if len(self._logger.handlers) > 0:
            # This logger already exists!  We don't support *updating* a logger by re-instantiation"
            return

        # Set default log level - Only process logs at this level or more severe
        self._logger.setLevel(config.default_level)

        # Ensure directories are created for log files
        self.create_directories(config.base_path)

        # Create the formatter for the logs
        # TODO Create colored logs
        self.formatter = logging.Formatter(
            "[%(asctime)s:%(levelname)-8s] %(name)s|%(funcName)s|> %(module)s.py:%(lineno)d -> %(message)s"
        )
        self.colored_formatter = ColoredFormatter(
            "%(log_color)s[%(asctime)s:%(levelname)-8s] %(name)s|%(funcName)s|> %(module)s.py:%(lineno)d -> %(reset)s%(message)s",
            reset=True,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )

        # Create Info and Debug file handlers
        self.create_file_handler(level=logging.DEBUG)
        self.create_file_handler(level=logging.INFO)

        # Stream Handler for light messaging
        self.create_stream_handler()

        # Loki Handler for posting logs directly to Loki
        loki_handler = self.get_loki_handler(config)
        if loki_handler:
            loki_handler.setLevel(config.default_level)
            loki_handler.setFormatter(self.formatter)
            self._logger.addHandler(loki_handler)

        logging.addLevelName(self.VERBOSE, "VERBOSE-1")

    def create_stream_handler(self,
                              level=None,
                              formatter=None,
                              stream=None) -> logging.StreamHandler:
        """
        Create a stream handler for the logger 
        """
        level = level or self.config.stream_level
        formatter = formatter or (self.colored_formatter if
                                  self.config.stream_color else self.formatter)
        stream = stream or sys.stdout
        handler = logging.StreamHandler(stream)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        return handler

    def create_file_handler(self,
                            filename=None,
                            level=None,
                            formatter=None) -> RotatingFileHandler:
        """
        Create a rotating file handler for the logger
        """
        name_lookup = {
            self.CRITICAL: "Critical",
            self.ERROR: "Error",
            self.WARNING: "Warning",
            self.INFO: "Info",
            self.DEBUG: "Debug",
            self.VERBOSE: "Verbose",
        }
        filename = (
            filename or
            f"{self.config.base_path}/{name_lookup[level]}/{self.config.app_name}_{name_lookup[level].lower()}.log"
        )
        level = level or self.config.default_level
        formatter = formatter or self.formatter
        handler = RotatingFileHandler(filename=filename,
                                      maxBytes=1000000,
                                      backupCount=100,
                                      encoding="utf-8")
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        return handler

    def get_loki_handler(self, kwargs: LoggerKwargs):
        """
        Get handler for emitting messages to a Loki log server
        """
        if not kwargs.grafana_loki_endpoint:
            return None

        emitter.LokiEmitter.level_tag = "level"    # Tells Loki how to find log level?  Is this needed?  TODO
        handler = LokiHandler(
            url=kwargs.grafana_loki_endpoint,
        #tags={"orgID": "1", "application": "AOC2022"}, # TODO make this configurable
            tags={
                "orgID": "1",
                "UUID": str(kwargs.uuid)
            },
            version="1",
        )
        return handler

    def create_directories(self, base_path):
        """ Ensure directories for the log files are availalbe """
        for subpath in ["Info", "Debug"]:
            path = os.path.join(base_path, subpath)
            try:
                os.makedirs(path)
            except FileExistsError:
                continue

    def __getattr__(self, name):
        """ Passes calls through to Logger._logger object """
        if self._logger and hasattr(self._logger, name):
            return getattr(self._logger, name)
        raise AttributeError(f"Logger has no attribute '{name}'")

    def verbose(self, msg, *args, **kwargs):
        self._logger.log(self.VERBOSE, msg, *args, **kwargs)

    def close(self):
        while len(self._logger.handlers) > 0:
            handler = self._logger.handlers[0]
            self._logger.removeHandler(handler)
            handler.close()

        del self._logger

    def pretty(self, loglevel: int, object, *args, **kwargs):
        """
        Pretty logging for nested objects
        Use Logger.INFO/DEBUG/VERBOSE etc. for loglevel
        """

        formatted_record = pprint.pformat(object, indent=4).split("\n")
        for line in formatted_record:
            self._logger.log(loglevel, line, stacklevel=2, *args, **kwargs)


class TimeSeriesLogger:
    #from datetime import datetime
    #from influxdb_client import InfluxDBClient, Point
    #from influxdb_client.client.write_api import SYNCHRONOUS
    #from datetime import datetime
    #
    #
    #from cb_secrets import INFLUXDB2_BUCKET, INFLUXDB2_TOKEN, INFLUXDB2_ORG, INFLUXDB2_URL
    ##query_api = client.query_api()
    #
    #def record_price_data(type, value, symbol="BTC", brokerage="CoinbasePro", category="Crypto"):
    #    """ type should be either Price or Balance """
    #    with InfluxDBClient(url=INFLUXDB2_URL, token=INFLUXDB2_TOKEN, org=INFLUXDB2_ORG) as client:
    #        with client.write_api(write_options=SYNCHRONOUS) as write_api:
    #            tags = {
    #                "Category": category,
    #                "Brokerage": brokerage,
    #                "Symbol": symbol,
    #            }
    #            fields = {
    #                type.lower(): value
    #            }
    #            timestamp = datetime.now().astimezone()
    #            """
    #            The expected dict structure is:
    #            - measurement
    #            - tags
    #            - fields
    #            - time"""
    #            p = Point.from_dict({"measurement": type,
    #                                "tags": tags,
    #                                "fields": fields,
    #                                "time": timestamp})
    #            write_api.write(bucket=INFLUXDB2_BUCKET, record=p)
    pass
