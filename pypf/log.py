"""Class to provide logging functionality."""
import logging


class Log(object):
    """The Log object."""

    def __init__(self, name=__name__, level=30):
        """Initialize the logging object."""
        self._logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(name)-15s %(message)s',
                                      '%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(level)

    def debug(self, message):
        """Log debug messages."""
        self._logger.debug(message)

    def info(self, message):
        """Log informational messages."""
        self._logger.info(message)

    def warning(self, message):
        """Log warning messages."""
        self._logger.warning(message)

    def error(self, message):
        """Log error messages."""
        self._logger.error(message)

    def set_level(self, level):
        """Set the level of the logger."""
        self._logger.setLevel(level)
