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

    # TODO(me) Add properties to access attributes.
    def __init__(self, symbol, force_download=False, force_cache=False,
                 interval='1d', period=10):
        """Initialize the common functionality for all Instruments."""
        self.historical_data = OrderedDict()
        self.home_directory = os.path.expanduser('~/.pypf')
        self.historical_directory = os.path.join(self.home_directory, 'data')
        if os.path.isdir(self.historical_directory) is False:
            logging.info('creating data directory '
                         + self.historical_directory)
            os.makedirs(self.historical_directory)

        self.force_download = force_download
        self.force_cache = force_cache
        if interval not in ["1d", "1wk", "1mo"]:
            logging.info("incorrect interval: "
                         "valid intervals are 1d, 1wk, 1mo")
            raise ValueError()
        self.interval = interval
        self.period = period

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
            if os.path.isfile(self.symbol_file):
                modification_time = os.path.getmtime(self.symbol_file)
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

    def __init__(self, symbol, force_download=False, force_cache=False,
                 interval='1d', period=10):
        """Initialize the security.

        Use force_download and force_cache to set download behavior.
        """
        super().__init__(symbol, force_download, force_cache, interval, period)
        self.symbol = symbol.lower().replace('.', '-')
        self.symbol_file = os.path.join(self.historical_directory,
                                        self.symbol
                                        + '_' + self.interval
                                        + '_yahoo'
                                        + '.csv')
        self.api_url = ("https://query1.finance.yahoo.com/v7/finance/download/"
                        "%s?period1=%s&period2=%s&interval=%s"
                        "&events=history&crumb=%s")

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
        self.cookie, self.crumb = self._get_cookie_crumb()
        now = datetime.datetime.now()
        m = now.month
        d = now.day
        y = now.year - self.period
        self.start = int(time.mktime(datetime.datetime(y, m, d).timetuple()))
        self.end = int(time.time())
        self.interval = self.interval
        url = self.api_url % (self.symbol, self.start, self.end,
                              self.interval, self.crumb)
        data = requests.get(url, cookies={'B': self.cookie})
        content = StringIO(data.content.decode("utf-8"))
        with open(self.symbol_file, 'w', newline='') as csvfile:
            for row in content.readlines():
                csvfile.write(row)
        return True
