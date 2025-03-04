"""Implementation of the system log."""

import logging

from prettyconf import config


class Logger:
    """A logger utility class for logging messages.

    This class provides an interface to log messages at different log levels
    (debug, info, warning, error, critical). It uses Python's built-in logging
    module and is configured to print logs to the console with a custom format.
    """

    def __init__(self, name_call: str) -> None:
        """Initialize the Logger class.

        Sets up the logging configuration with a custom format, logging level,
        and console handler.

        Arguments:
            name_call (str): The name for the logger. This name will appear in
                the log output to help identify the source of the log.

        Returns:
            None: Method without data return.

        """
        self.AMBIENT_ENV = config("AMBIENT_ENV", default=None)
        self.LOG_NAME = config("LOG_NAME", default="SDC")
        self.tip_logs = logging.getLogger(name_call)
        self.tip_logs.setLevel(logging.DEBUG)


        if not self.tip_logs.handlers:
            stream_format = logging.Formatter(
                f"{self.LOG_NAME}: time=%(asctime)s log_level=%(levelname)s "
                f"ref=api-data ambient={self.AMBIENT_ENV} nivel=3 "
                f"origin=%(name)s message=%(message)s",
                datefmt="%d/%m/%Y %H:%M:%S",
            )
            stream = logging.StreamHandler()
            stream.setLevel(logging.DEBUG)
            stream.setFormatter(stream_format)
            self.tip_logs.addHandler(stream)

    def debug(self, msg: str) -> None:
        """Log a debug message.

        Arguments:
            msg (str): The message to log.

        Returns:
            None: Method without data return.

        """
        self.tip_logs.debug(msg)

    def info(self, msg: str) -> None:
        """Log an info message.

        Arguments:
            msg (str): The message to log.

        Returns:
            None: Method without data return.

        """
        self.tip_logs.info(msg)

    def warning(self, msg: str) -> None:
        """Log a warning message.

        Arguments:
            msg (str): The message to log.

        Returns:
            None: Method without data return.

        """
        self.tip_logs.warning(msg)

    def error(self, msg: str) -> None:
        """Log an error message.

        Arguments:
            msg (str): The message to log.

        Returns:
            None: Method without data return.

        """
        self.tip_logs.error(msg)

    def critical(self, msg: str) -> None:
        """Log a critical message.

        Arguments:
            msg (str): The message to log.

        Returns:
            None: Method without data return.

        """
        self.tip_logs.critical(msg)
