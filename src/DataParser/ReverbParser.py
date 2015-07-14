__author__ = 'tmy'

import logging
import pandas as pd
from ext2rdf.src.DataParser.AbstractParser import AbstractParser
from ext2rdf.src.Utilities.Constants import LOG_LEVEL

log = logging.getLogger()
log.setLevel(LOG_LEVEL)

pd.options.display.max_rows = 1000


class DataParser(AbstractParser):
    def parse(self, path):
        pass
