import logging
from logging.handlers import RotatingFileHandler
import sys
from dataclasses import dataclass
from typing import Protocol
import os
import pprint


from colorlog import ColoredFormatter
from logging_loki import LokiHandler, emitter
from uuid import UUID, uuid1


@dataclass
class LoggerKwargs:
    app_name: str = "default_logger"
    default_level: int = logging.DEBUG
    stream_color: bool = None
    stream_level: int = logging.INFO
    grafana_loki_endpoint: str = ""
    grafana_tempo_endpoint: str = ""
    uuid: UUID = uuid1()


class LoggerInfo(Protocol):

    @property
    def app_name(self) -> str:
        ...

    @property
    def default_level(self) -> int:
        ...


class Logger:
    """
    Opinionated logger with built in creature comforts

    kwargs:
        stream_color bool: turns on or off terminal colors for stream handler
        stream_level int: Sets the logging level for the stream handler
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

    def __init__(self, info: LoggerInfo = None, **kwargs):
        # Handle LoggerInfo or Legacy kwargs implementation
        if info is None:
            info = LoggerKwargs(**kwargs)

        # Create logger based on application name
        self.app_name = info.app_name
        self._logger = logging.getLogger(self.app_name)

        if len(self._logger.handlers) > 0:
            # This logger already exists!  We don't support *updating* a logger by re-instantiation")
            return

        # Set default log level - Only process logs at this level or more severe
        self._logger.setLevel(info.default_level)

        # Ensure directories are created for log files (Can this be configured?  To not happen automatically?)
        self.create_directories()

        # Create the formatter for the logs
        # TODO Create colored logs
        formatter = logging.Formatter(
            '[%(asctime)s:%(levelname)-8s] %(name)s.%(module)s.%(funcName)s:%(lineno)d -> %(message)s'
        )
        formatter_c = ColoredFormatter(
            '%(log_color)s[%(asctime)s:%(levelname)-8s] %(name)s.%(module)s.%(funcName)s:%(lineno)d -> %(reset)s%(message)s',
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
        )

        # Rotating file handler for debug messages
        debug_file_handler = RotatingFileHandler(
            filename=f'Logs/Debug/{info.app_name}_debug.log',
            maxBytes=1000000,
            backupCount=100)
        debug_file_handler.setLevel(logging.DEBUG)
        debug_file_handler.setFormatter(formatter)

        # Rotating file handler for info messages
        info_file_handler = RotatingFileHandler(
            filename=f'Logs/Info/{info.app_name}_info.log',
            maxBytes=1000000,
            backupCount=100)
        info_file_handler.setLevel(logging.INFO)
        info_file_handler.setFormatter(formatter)

        # Stream Handler for light messaging
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(info.stream_level)
        if info.stream_color:
            stream_handler.setFormatter(formatter_c)
        else:
            stream_handler.setFormatter(formatter)

        # Loki Handler for posting logs directly to Loki
        loki_handler = self.get_loki_handler(info)
        if loki_handler:
            loki_handler.setLevel(info.default_level)
            loki_handler.setFormatter(formatter)

        # Add the log handlers to the logger
        self._logger.addHandler(debug_file_handler)
        self._logger.addHandler(info_file_handler)
        self._logger.addHandler(stream_handler)

        if loki_handler:
            self._logger.addHandler(loki_handler)

        logging.addLevelName(self.VERBOSE, "VERBOSE-1")

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
            tags={"orgID": "1", "UUID": str(kwargs.uuid)},
            version="1",
        )
        return handler

    def create_directories(self):
        """ Ensure directories for the log files are availalbe """
        for subpath in ["Logs/Info", "Logs/Debug"]:
            path = os.path.join(os.getcwd(), subpath)
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
