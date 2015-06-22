__author__ = 'tmy'

import os
import logging
import pandas as pd
import numpy as np
import csv
from Utilities.Constants import config, programs

log = logging.getLogger()
log.setLevel(config['app']['app_log_level'])

pd.options.display.max_rows = 1000


class DataParser(object):

    def parse(self, program=programs['oIE'], path=config['app']['data_path']):
        if not os.path.isfile(path):
            raise IOError("a valid file path must be given")
        with open(path, mode='r', encoding='utf-8') as f:
            log.info("parsing file: {}".format(f))
            if program == programs['oIE']:
                return self.__openie_parse(f)
            elif program == programs['rvb']:
                return self.__reverb_parse(f)
            else:
                raise ValueError("program must be of valid entry")

    @staticmethod
    def __openie_parse(f):
        columns = ['confidence', 'context', 'arg1', 'rel', 'arg2s', 'sentence_id', 'sentence']
        values = pd.read_csv(f, sep='\t', names=columns, header=None, quoting=csv.QUOTE_NONE)
        return values.dropna(subset=['arg1', 'rel', 'arg2s'])

    @staticmethod
    def __reverb_parse(f):
        data = {}
        # TODO
        return data