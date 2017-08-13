"""Classes to represent financial instruments."""
from abc import ABCMeta
from abc import abstractmethod
from collections import OrderedDict
from decimal import Decimal

import csv
import datetime
import logging
import os
import sys

if sys.platform != 'ios':
    # ugly hack but it lets us develop on ios.
    # the cython parts of pandas are not supported and will break on import.
    from pandas_datareader._utils import RemoteDataError
    import pandas_datareader.data as web


class Instrument(metaclass=ABCMeta):
    """Base class for all Instruments."""

    # TODO(me) Add properties to access attributes.
    def __init__(self, symbol, force=False, cache=False, period=5):
        """Initialize the common functionality for all Instruments."""
        now = datetime.datetime.now()
        self.home_directory = os.path.expanduser('~/.pypf')
        self.historical_directory = os.path.join(self.home_directory, 'data')
        if os.path.isdir(self.historical_directory) is False:
            logging.info('creating data directory '
                         + self.historical_directory)
            os.makedirs(self.historical_directory)
        self.symbol = symbol.lower().replace('.', '-')
        self.symbol_file = os.path.join(self.historical_directory,
                                        self.symbol + '.csv')
        self.month = now.month
        self.day = now.day
        self.to_year = now.year
        self.from_year = now.year - period
        self.historical_data = OrderedDict()
        self.force = force
        self.cache = cache
        # force the use of cache on ios since pandas is not supported.
        # this will prevent _download_data from being called.
        if sys.platform == 'ios':
            self.cache = True

    def populate_data(self):
        """Populate the instrument with data.

        Data will only be downloaded if the data file doesn't exist or
        if the modification time of the file does not equal the current
        date. This behavior can be overridden with the --force-cache
        and --force-download options.
        """
        # TODO(me): Refactor without using exceptions.
        download_data = False

        if self.force:
            download_data = True
        else:
            if os.path.isfile(self.symbol_file):
                modification_time = os.path.getmtime(self.symbol_file)
                last_modified_date = (datetime.date
                                      .fromtimestamp(modification_time))
                today = datetime.datetime.now().date()

                if last_modified_date != today:
                    download_data = True
            else:
                download_data = True

        if self.cache:
            download_data = False

        if download_data:
            logging.info('downloading historical data for ' + self.symbol)
            try:
                self._download_data()
            except Exception:
                # should be RemoteDataError if pandas worked on ios
                logging.info('unable to download data for ' + self.symbol)
                raise
            csv_file = open(self.symbol_file, newline='')
        else:
            logging.info('using cached historical data for ' + self.symbol)
            try:
                csv_file = open(self.symbol_file, newline='')
            except FileNotFoundError:
                logging.info('no data exists in the cache for ' + self.symbol)
                raise

        reader = csv.DictReader(csv_file)
        for row in reader:
            factor = Decimal(row['Adj Close']) / Decimal(row['Close'])
            row['Open'] = Decimal(row['Open']) * factor
            row['High'] = Decimal(row['High']) * factor
            row['Low'] = Decimal(row['Low']) * factor
            row['Close'] = Decimal(row['Close']) * factor
            row['Volume'] = Decimal(row['Volume'])
            row.pop('Adj Close', None)
            self.historical_data[row['Date']] = row

    @abstractmethod
    def _download_data(self):
        """To be implemented in derived classes.

        Data must be stored in a csv file that follows the Yahoo format, which
        includes an Adjusted Close field. If the data is already Adjusted
        then include Adjusted Close field that equals the Close field.
        """
        pass


class Security(Instrument):
    """Security instrument that uses Yahoo as the datasource."""

    def __init__(self, symbol, force=False, cache=False, period=5):
        """Initialize the security.

        Use the force and cache options to set download behavior.
        """
        super().__init__(symbol, force, cache, period)

    def __str__(self):
        """Return the symbol of the security."""
        return self.symbol

    def _download_data(self):
        start = datetime.datetime(self.from_year, self.month, self.day)
        end = datetime.datetime(self.to_year, self.month, self.day)
        h = web.DataReader(self.symbol, 'yahoo', start, end)
        h.to_csv(self.symbol_file)
        return True
