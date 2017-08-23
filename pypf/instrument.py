"""Classes to represent financial instruments."""
from abc import ABCMeta
from abc import abstractmethod
from collections import OrderedDict
from decimal import Decimal
from io import StringIO

import csv
import datetime
import logging
import os
import re
import requests
import time


class Instrument(metaclass=ABCMeta):
    """Base class for all Instruments."""

    def __init__(self, symbol, force_download=False, force_cache=False,
                 interval='1d', period=10, data_directory='~/.pypf/data',
                 data_file=''):
        """Initialize the common functionality for all Instruments."""
        self._data_directory = ''
        self._data_file = ''

        self.data_directory = data_directory
        self.data_file = data_file
        self.force_cache = force_cache
        self.force_download = force_download
        self.historical_data = OrderedDict()
        self.interval = interval
        self.period = period
        self.symbol = symbol

    @property
    def data_directory(self):
        """Set the directory in which to store historical data."""
        return self._data_directory

    @data_directory.setter
    def data_directory(self, value):
        value = os.path.expanduser(value)
        if os.path.isdir(value) is False:
            logging.info('creating data directory ' + value)
            os.makedirs(value)
        self._data_directory = value
        self._data_path = os.path.join(value, self.data_file)

    @property
    def data_file(self):
        """Set the file name that contains the historical data."""
        return self._data_file

    @data_file.setter
    def data_file(self, value):
        self._data_file = value
        self._data_path = os.path.join(self.data_directory, value)

    @property
    def data_path(self):
        """Get the full path of the data file."""
        return self._data_path

    @property
    def force_cache(self):
        """Force use of cached data."""
        return self._force_cache

    @force_cache.setter
    def force_cache(self, value):
        self._force_cache = value

    @property
    def force_download(self):
        """Force download of data."""
        return self._force_download

    @force_download.setter
    def force_download(self, value):
        self._force_download = value

    @property
    def interval(self):
        """Specify day (1d), week (1wk), or month (1mo) interval."""
        return self._interval

    @interval.setter
    def interval(self, value):
        if value not in ["1d", "1wk", "1mo"]:
            raise ValueError("incorrect interval: "
                             "valid intervals are 1d, 1wk, 1mo")
        self._interval = value

    @property
    def period(self):
        """Set the years of data to download."""
        return self._period

    @period.setter
    def period(self, value):
        if value <= 0:
            raise ValueError('period must be greater than 0.')
        self._period = value
        now = datetime.datetime.now()
        m = now.month
        d = now.day
        y = now.year - value
        self._start_date = int(time.mktime(datetime
                                           .datetime(y, m, d).timetuple()))
        self._end_date = int(time.time())

    @property
    def symbol(self):
        """Set the symbol of the instrument."""
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        self._symbol = value.upper()

    def populate_data(self):
        """Populate the instrument with data.

        Data will only be downloaded if the data file doesn't exist or
        if the modification time of the file does not equal the current
        date. This behavior can be overridden with the --force-cache
        and --force-download options.
        """
        # TODO(me): Refactor without using exceptions.
        download_data = False

        if self.force_download:
            download_data = True
        else:
            if os.path.isfile(self.data_path):
                modification_time = os.path.getmtime(self.data_path)
                last_modified_date = (datetime.date
                                      .fromtimestamp(modification_time))
                today = datetime.datetime.now().date()

                if last_modified_date != today:
                    download_data = True
            else:
                download_data = True

        if self.force_cache:
            download_data = False

        if download_data:
            logging.info('downloading historical data for ' + self.symbol)
            self._download_data()
            csv_file = open(self.data_path, newline='')
        else:
            logging.info('using cached historical data for ' + self.symbol)
            csv_file = open(self.data_path, newline='')

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

    def __init__(self, symbol, force_download=False, force_cache=False,
                 interval='1d', period=10, data_directory='~/.pypf/data'):
        """Initialize the security."""
        super().__init__(symbol, force_download, force_cache,
                         interval, period, data_directory)
        self.symbol = self.symbol.replace('.', '-')
        self.data_file = (self.symbol
                          + '_' + self.interval
                          + '_yahoo'
                          + '.csv')

    def _get_cookie_crumb(self):
        """Return a tuple pair of cookie and crumb used in the request."""
        url = 'https://finance.yahoo.com/quote/%s/history' % (self.symbol)
        r = requests.get(url)
        txt = r.content
        cookie = r.cookies['B']
        pattern = re.compile('.*"CrumbStore":\{"crumb":"(?P<crumb>[^"]+)"\}')

        for line in txt.splitlines():
            m = pattern.match(line.decode("utf-8"))
            if m is not None:
                crumb = m.groupdict()['crumb']
                crumb = crumb.replace(u'\\u002F', '/')
        return cookie, crumb

    def _download_data(self):
        cookie, crumb = self._get_cookie_crumb()
        api_url = ("https://query1.finance.yahoo.com/v7/finance/"
                   "download/%s?period1=%s&period2=%s&interval=%s"
                   "&events=history&crumb=%s")
        url = api_url % (self.symbol, self._start_date, self._end_date,
                         self.interval, crumb)
        data = requests.get(url, cookies={'B': cookie})
        content = StringIO(data.content.decode("utf-8"))
        with open(self.data_path, 'w', newline='') as csvfile:
            for row in content.readlines():
                csvfile.write(row)
        return True
