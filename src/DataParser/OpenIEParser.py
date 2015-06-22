__author__ = 'tmy'

import os
import logging
import re
import pandas as pd
from DataParser.AbstractParser import AbstractParser
from Extraction.Extraction import Extraction
import csv
from Utilities.Constants import config, arg_types

log = logging.getLogger()
log.setLevel(config['app']['app_log_level'])

pd.options.display.max_rows = 1000

arg_pattern = r'^SimpleArgument\(([0-9]*\s+)?'
list_pattern = r',List\(.*\)$'
relation_pattern = r'^Relation\('
context_pattern = r'^Context\(([0-9]*\s+)?'
temporal_pattern = r'^TemporalArgument\('
spatial_pattern = r'^SpatialArgument\('
arg2s_split_pattern = r'; (SimpleArgument|TemporalArgument|SpatialArgument)'


def convert_arg(arg):
    if re.match(relation_pattern, arg):
        cleaned_arg = re.sub(relation_pattern + '|' + list_pattern, '', arg)
        return {'type': arg_types['rel'], 'cleaned_arg': cleaned_arg}
    elif re.match(arg_pattern, arg):
        cleaned_arg = re.sub(arg_pattern + '|' + list_pattern, '', arg)
        return {'type': arg_types['simple'], 'cleaned_arg': cleaned_arg}
    elif re.match(temporal_pattern, arg):
        cleaned_arg = re.sub(temporal_pattern + '|' + list_pattern, '', arg)
        return {'type': arg_types['tmp'], 'cleaned_arg': cleaned_arg}
    elif re.match(spatial_pattern, arg):
        cleaned_arg = re.sub(spatial_pattern + '|' + list_pattern, '', arg)
        return {'type': arg_types['spatial'], 'cleaned_arg': cleaned_arg}
    else:
        log.warn("For argument: {}".format(arg))
        raise ValueError("tried to convert malformed argument")


class DataParser(AbstractParser):

    def __init__(self):
        pass

    def parse(self, path=config['app']['data_path']):
        if not os.path.isfile(path):
            raise IOError("a valid file path must be given")
        with open(path, mode='r', encoding='utf-8') as f:
            log.info("parsing file: {}".format(f))
            return self.__openie_parse(f)

    @staticmethod
    def __openie_parse(f):
        columns = ['confidence', 'context', 'arg1', 'rel', 'arg2s', 'sentence_id', 'sentence']
        values = pd.read_csv(f, sep='\t', names=columns, header=None, quoting=csv.QUOTE_NONE)
        values = values.dropna(subset=['arg1', 'rel', 'arg2s'])
        extractions = []
        for _, row in values.iterrows():
            data = {'temporal_args': [], 'additional_args': [], 'spatial_args': []}
            if 'arg2s' in row and not pd.isnull(row['arg2s']):
                arg2s = re.split(arg2s_split_pattern, row['arg2s'])
                for index, arg in enumerate(arg2s):
                    if arg == "SimpleArgument" or arg == "TemporalArgument" or arg == "SpatialArgument":
                        arg2s[index + 1] = arg + arg2s[index + 1]
                    else:
                        converted_arg = convert_arg(arg)
                        if index == 0:
                            data['object'] = converted_arg['cleaned_arg']
                        else:
                            if converted_arg['type'] == arg_types['simple']:
                                data['additional_args'].append(converted_arg['cleaned_arg'])
                            elif converted_arg['type'] == arg_types['tmp']:
                                data['temporal_args'].append(converted_arg['cleaned_arg'])
                            elif converted_arg['type'] == arg_types['spatial']:
                                data['spatial_args'].append(converted_arg['cleaned_arg'])

            elif 'arg2' in row and not pd.isnull(row['arg2']):
                converted_arg = convert_arg(row['arg2'])
                data['object'] = converted_arg['cleaned_arg']
            else:
                pass
            converted_pred = convert_arg(row['rel'])
            data['predicate'] = converted_pred['cleaned_arg']
            converted_sub = convert_arg(row['arg1'])
            data['subject'] = converted_sub['cleaned_arg']
            if not pd.isnull(row['context']):
                context = re.sub(context_pattern + '|' + list_pattern, '', row['context'])
                data['context'] = context
            else:
                data['context'] = ""
            data['confidence'] = row['confidence']
            data['sentence_id'] = row['sentence_id']
            data['sentence'] = row['sentence']
            extractions.append(Extraction(data))
        return extractions