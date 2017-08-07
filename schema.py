"""This is the docstring."""
import os


class TradeMeta(object):
    """Deprecated class that will be removed."""

    def __init__(self):
        """Deprecated."""
        self.home_directory = '.'
        self.data_directory = os.path.join(self.home_directory, 'data')
        self.historical_directory = os.path.join(self.home_directory,
                                                 'data', 'historical')
