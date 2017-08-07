from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from decimal import Decimal
from pandas_datareader._utils import RemoteDataError
import csv
import datetime
import logging
import pandas_datareader.data as web
import os


class Instrument(metaclass=ABCMeta):
    def __init__(self, symbol, force=False, cache=False, period=5):
        now = datetime.datetime.now()
        self.home_directory = '.'
        self.historical_directory = os.path.join(self.home_directory, 'data')
        self.symbol = symbol.lower().replace('.', '-')
        self.symbol_file = os.path.join(self.historical_directory, self.symbol + '.csv')
        self.month = now.month
        self.day = now.day
        self.to_year = now.year
        self.from_year = now.year - period
        self.historical_data = OrderedDict()
        self.force = force
        self.cache = cache

    def populate_data(self):
        download_data = False

        if self.force:
            download_data = True
        else:
            if os.path.isfile(self.symbol_file):
                modification_time = os.path.getmtime(self.symbol_file)
                last_modified_date = datetime.date.fromtimestamp(modification_time)
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
                self.download_data()
            except RemoteDataError:
                logging.info('unable to download historical data for ' + self.symbol)
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
    def download_data(self):
        pass


class Security(Instrument):
    def __init__(self, symbol, force=False, cache=False, period=5):
        super().__init__(symbol, force, cache, period)

    def __str__(self):
        return self.symbol

    def download_data(self):
        start = datetime.datetime(self.from_year, self.month, self.day)
        end = datetime.datetime(self.to_year, self.month, self.day)
        h = web.DataReader(self.symbol, 'yahoo', start, end)
        h.to_csv(self.symbol_file)
        return True
