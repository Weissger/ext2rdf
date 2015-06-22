__author__ = 'tmy'

import logging
import pandas as pd
from DataParser.AbstractParser import AbstractParser
from Utilities.Constants import config

log = logging.getLogger()
log.setLevel(config['app']['app_log_level'])

pd.options.display.max_rows = 1000


class DataParser(AbstractParser):

    def parse(self, path=config['app']['data_path']):
        pass