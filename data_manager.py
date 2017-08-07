"""This is the docstring."""
# TODO(me): Refactor this file to be a generic download manager
# from instrument import Security
from schema import TradeMeta

import datetime
import logging
import os
import urllib.request


class DownloadError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class DataManager(TradeMeta):
    def __init__(self, spdrs=[], period=5):
        super().__init__()
        self.period = period
        now = datetime.datetime.now()
        self.month = str(now.month)
        self.day = str(now.day)
        self.to_year = str(now.year)
        self.from_year = str(now.year - self.period)
        self.spdrs = spdrs

    def delete_historical_data(self):
        logging.warning('deleting existing historical data')
        directory = self.historical_directory
        for file in os.listdir(directory):
            if file[-3:] != 'csv':
                continue
            if os.path.isfile(os.path.join(directory, file)):
                try:
                    os.remove(os.path.join(directory, file))
                except FileNotFoundError:
                    pass

    def download_symbol(self, security):
        # rewrite using new Yahoo API
        pass

    def download_data(self):
        logging.warning('downloading historical data to '
                        + self.historical_directory)
        self.delete_historical_data()

        failures = []
        seen = []
        for spdr in self.spdrs:
            logging.warning('processing ' + spdr.symbol)
            spdr.populate_holdings()
            holdings = spdr.holdings
            holdings.append(Security(spdr.symbol))
            for security in holdings:
                if security.symbol not in seen:
                    result = self.download_symbol(security)
                    if not result:
                        failures.append(security)
                    seen.append(security.symbol)

        second_failures = []
        for security in failures:
            logging.warning('retrying download of ' + security.symbol)
            result = self.download_symbol(security)
            if not result:
                second_failures.append(security)

        if len(second_failures) > 0:
            raise DownloadError('second attempt failed to download: ' + str(second_failures))

    def retrieve_holdings(self):
        logging.warning('downloading spdr holdings files to ' + self.data_directory)
        failures = []
        for spdr in self.spdrs:
            url = spdr.url
            holdings_file = os.path.join(self.data_directory, spdr.symbol + '_holdings.xls')
            logging.info('downloading ' + spdr.symbol)
            try:
                os.remove(holdings_file)
            except FileNotFoundError:
                logging.info(holdings_file + ' was not deleted because it does not exist')

            try:
                print(url)
                urllib.request.urlretrieve(url, holdings_file)
            except urllib.request.ContentTooShortError:
                logging.warning('failed to download holdings file for ' + spdr.symbol)
                failures.append(spdr)

        second_failures = []
        for spdr in failures:
            url = spdr.url
            holdings_file = os.path.join(self.data_directory, spdr.symbol + '_holdings.xls')
            logging.warning('retrying download of ' + spdr.symbol)
            try:
                urllib.request.urlretrieve(url, holdings_file)
            except urllib.request.ContentTooShortError:
                second_failures.append(spdr)

        if len(second_failures) > 0:
            raise DownloadError('spdr holdings failed to download: ' + str(second_failures))
