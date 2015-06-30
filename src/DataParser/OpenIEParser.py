__author__ = 'tmy'

import os
import logging
import re
import pandas as pd
from DataParser.AbstractParser import AbstractParser
from Extraction.Extraction import Extraction
import csv
from Utilities.Constants import config, ARG_TYPES
from Utilities.Lemmatizer import Lemmatizer

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


class DataParser(AbstractParser):

    def __init__(self):
        self.__counter = {
            'missing_objects': 0,
            'missing_contexts': 0,
            'temporal_arguments': 0,
            'spatial_arguments': 0,
            'simple_arguments': 0,
            'extractions': 0
        }
        self.__lemmatizer = Lemmatizer()

    def parse(self, path=config['app']['data_path']):
        if not os.path.isfile(path):
            raise IOError("a valid file path must be given")
        with open(path, mode='r', encoding='utf-8') as f:
            log.info("parsing file: {}".format(f))
            return self.__openie_parse(f)

    def __openie_parse(self, f):
        columns = ['confidence', 'context', 'arg1', 'rel', 'arg2s', 'sentence_id', 'sentence']
        values = pd.read_csv(f, sep='\t', names=columns, header=None, quoting=csv.QUOTE_NONE)
        extractions = []
        for _, row in values.iterrows():
            data = {'temporal_args': [], 'additional_args': [], 'spatial_args': []}
            if 'arg2s' in row and not pd.isnull(row['arg2s']):
                arg2s = re.split(arg2s_split_pattern, row['arg2s'])
                for index, arg in enumerate(arg2s):
                    if arg == "SimpleArgument" or arg == "TemporalArgument" or arg == "SpatialArgument":
                        arg2s[index + 1] = arg + arg2s[index + 1]
                    else:
                        converted_arg = self.__convert_arg(arg)
                        if index == 0:
                            data['object'] = converted_arg['cleaned_arg']
                        else:
                            if converted_arg['type'] == ARG_TYPES['simple']:
                                data['additional_args'].append(converted_arg['cleaned_arg'])
                            elif converted_arg['type'] == ARG_TYPES['tmp']:
                                data['temporal_args'].append(converted_arg['cleaned_arg'])
                            elif converted_arg['type'] == ARG_TYPES['spatial']:
                                data['spatial_args'].append(converted_arg['cleaned_arg'])

            elif 'arg2' in row and not pd.isnull(row['arg2']):
                converted_arg = self.__convert_arg(row['arg2'])
                data['object'] = converted_arg['cleaned_arg']
            else:
                self.__counter['missing_objects'] += 1
                continue
            converted_pred = self.__convert_arg(row['rel'])
            data['predicate'] = converted_pred['cleaned_arg']
            data['predicate_lemma'] = self.__lemmatizer.lemmatize(converted_pred['cleaned_arg'])
            converted_sub = self.__convert_arg(row['arg1'])
            data['subject'] = converted_sub['cleaned_arg']
            if not pd.isnull(row['context']):
                context = re.sub(context_pattern + '|' + list_pattern, '', row['context'])
                data['context'] = context
            else:
                data['context'] = ""
                self.__counter['missing_contexts'] += 1
            data['confidence'] = row['confidence']
            data['sentence_id'] = row['sentence_id']
            data['sentence'] = row['sentence']
            extractions.append(Extraction(data))

        self.__counter['simple_arguments'] -= len(extractions)
        self.__counter['extractions'] = len(extractions)
        return extractions

    def __convert_arg(self, arg):
        if re.match(relation_pattern, arg):
            cleaned_arg = re.sub(relation_pattern + '|' + list_pattern + '|' + r'\[|\]', '', arg)
            return {'type': ARG_TYPES['rel'], 'cleaned_arg': cleaned_arg}
        elif re.match(arg_pattern, arg):
            self.__counter['simple_arguments'] += 1
            cleaned_arg = re.sub(arg_pattern + '|' + list_pattern, '', arg)
            return {'type': ARG_TYPES['simple'], 'cleaned_arg': cleaned_arg}
        elif re.match(temporal_pattern, arg):
            self.__counter['temporal_arguments'] += 1
            cleaned_arg = re.sub(temporal_pattern + '|' + list_pattern, '', arg)
            return {'type': ARG_TYPES['tmp'], 'cleaned_arg': cleaned_arg}
        elif re.match(spatial_pattern, arg):
            self.__counter['spatial_arguments'] += 1
            cleaned_arg = re.sub(spatial_pattern + '|' + list_pattern, '', arg)
            return {'type': ARG_TYPES['spatial'], 'cleaned_arg': cleaned_arg}
        else:
            log.warn("For argument: {}".format(arg))
            raise ValueError("tried to convert malformed argument")

    def get_counter(self):
        return self.__counter
