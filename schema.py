import os


class TradeMeta:
    def __init__(self):
        self.home_directory = '.'
        self.data_directory = os.path.join(self.home_directory, 'data')
        self.historical_directory = os.path.join(self.home_directory, 'data', 'historical')