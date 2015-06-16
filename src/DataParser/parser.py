__author__ = 'tmy'

import os
import logging
import pandas as pd
import csv
from Utilities.Constants import config

log = logging.getLogger()
log.setLevel(logging.DEBUG)

pd.options.display.max_rows = 1000


class DataParser(object):
    oIE = "openIE"
    rvb = "reverb"

    def parse(self, program=oIE, path=config['app']['data_path']):
        if not os.path.isfile(path):
            raise IOError("a valid file path must be given")
        with open(path, mode='r', encoding='utf-8') as f:
            if program == DataParser.oIE:
                return self.__openie_parse(f)
            elif program == DataParser.rvb:
                return self.__reverb_parse(f)
            else:
                raise ValueError("program must be of valid entry")

    @staticmethod
    def __openie_parse(f):
        log.info("parsing file: {}".format(f))
        values = pd.read_csv(f, sep='\t', header=None, quoting=csv.QUOTE_NONE)
        values.rename(
            columns={0: 'confidence', 1: 'context', 2: 'arg1', 3: 'rel', 4: 'arg2s', 5: 'sentence_id', 6: 'sentence'},
            inplace=True)
        return values

    @staticmethod
    def __reverb_parse(f):
        data = {}
        # TODO
        return data