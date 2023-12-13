""" Module for handling serial communication with devices"""
from typing import Optional
from queue import Queue, Empty
import re
import time
import threading

import serial
from pymccool.logging import Logger, LoggerKwargs

logger = Logger(LoggerKwargs(app_name="pyMcCool"))

class SerialDevice:
    """ Class representing a Serial COM device and the utiltities for communicating with it """
    def __init__(self,
                 port: str,
                 baudrate: int = 115200,
                 username: Optional[str] = None,
                 password: Optional[str] = None):
        """
        Instantiate the SerialDevice class
        :param port: String representation of COM Port, e.g. COM11
        :param baudrate: Baudrate of the device, defaults to 115200
        :param username: Username for device, if no username, no login is performed
        :param password: Password for device, if no password, no login is performed
        :return: SerialDevice instance
        """
        self.port = port
        self.baudrate = baudrate
        self.username = username # pi
        self.password = password # SQA

        self.interface: serial.Serial = None # Serial connection to the device
        self.active: bool = False # Flag to indicate if the device is active and connected
        self.t: Optional[threading.Thread] = None # Read Thread

        self.read_loop_finished: Queue = Queue() # Queue to pass between threads when finished
        self.line_ending = b"\r\n"
        self.buffer = bytes() # Buffer to hold data from the device
        self.q: Queue = Queue() # Queue to pass data from reader thread to main thread

        self.connect()

    def escape_ansi(self, line) -> str:
        logger.debug([b for b in line])
        ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
        return ansi_escape.sub('', str(line))


    def connect(self) -> None:
        """ Initiate connection to the device"""
        if self.interface is None:
            self.interface = serial.Serial(self.port, self.baudrate)
            self.active = True
            self.t = threading.Thread(target=self.reader)
            self.t.daemon = True

            # sync up
            time.sleep(0.1)
            data = self.interface.read(self.interface.in_waiting)
            i = data.find(b"\n")
            if i >= 0:
                self.buffer = data[i + 1:]

            self.t.start()

    def send_line(self, line):
        """
        Send command lines
        :param line: command str to send
        """
        self.interface.write(line.encode("utf-8") + self.line_ending)
        self.interface.flush()

    def reader(self):
        """Serial Data reader"""
        failures = 0
        while self.active:
            try:
                data = self.interface.read(self.interface.in_waiting or 1)
                self.buffer += data
                failures = 0
            except TypeError:
                # bizarre
                continue
            except serial.SerialException:
                failures += 1
                if failures > 32:
                    raise
                continue

            #logger.debug("Buffer: " + str(self.buffer))
            if self.line_ending in self.buffer:
                parts = self.buffer.split(self.line_ending, maxsplit=1)
                self.buffer = parts.pop()
                for part in parts:
                    part = part.decode('utf-8')
                    self.q.put(part)
                    logger.debug(part)


            # If there needs to be any special processing of the data, do it here
            #if len(line.strip()) == 0:
            #    continue
            # kf regex line == special case, do something

        self.read_loop_finished.put(True)