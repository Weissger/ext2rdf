#!/usr/bin/env python3

__author__ = 'tmy'

from Utilities.Constants import config, PROGRAMS, E2RDF_COLUMN_NAMES, SEPARATOR, CONVERTER_TYPES
from DataParser import OpenIEParser
from DataParser import ReverbParser
from RDFConverter import ReificationStructureConverter
from RDFConverter import TripleStructureConverter
from RDFConverter import SimpleStructureConverter
import csv
import pandas as pd
import logging
from io import StringIO

log = logging.getLogger()
log.setLevel(config['app']['app_log_level'])


def generate_e2rdf(extractions):
    s = StringIO("\n".join([e.to_e2rdf() for e in extractions]))
    return pd.read_csv(s, names=E2RDF_COLUMN_NAMES, sep=SEPARATOR, quoting=csv.QUOTE_NONE)


def write_to_disk(path, dataframe):
    filename = path + ".e2rdf"

    with open(filename, 'w') as _:
        pass
    with open(filename, "a") as f:
        for _, row in dataframe.iterrows():
            f.write(SEPARATOR.join(row.map(str)) + "\n")


def convert_output_file(path, out=config['app']['data_path'] + "output", serialization_format="nt",
                        converter_type=CONVERTER_TYPES['reification'], program=config['app']['program']):
    if program == PROGRAMS['oIE']:
        data_parser = OpenIEParser.DataParser()
    elif program == PROGRAMS['rvb']:
        data_parser = ReverbParser.DataParser()
    else:
        log.warn("Unknown program")
        return
    extractions = data_parser.parse(path)
    df = generate_e2rdf(extractions)

    # Subject length filter
    max_len = int(config['app']['max_subject_length'])
    if max_len > 0:
        df = df[df['Subject'].map(split, " ").map(len) <= max_len]

    # Predicate length filter
    max_len = int(config['app']['max_predicate_length'])
    if max_len > 0:
        df = df[df['Predicate'].map(split, " ").map(len) <= max_len]

    # Object length filter
    max_len = int(config['app']['max_object_length'])
    if max_len > 0:
        df = df[df['Object'].map(split, " ").map(len) <= max_len]

    write_to_disk(path[0:s.rfind('.')], df)

    if converter_type == CONVERTER_TYPES['reification']:
        rdf_converter = ReificationStructureConverter.Converter()
    elif converter_type == CONVERTER_TYPES['triple']:
        rdf_converter = TripleStructureConverter.Converter()
    elif converter_type == CONVERTER_TYPES['simple']:
        rdf_converter = SimpleStructureConverter.Converter()
    else:
        log.warn("Unknown converter type")
        return
    graph = rdf_converter.convert(df)
    graph.serialize(out + "." + serialization_format, serialization_format)

    log.warn([(e, data_parser.get_counter()[e]) for e in sorted(data_parser.get_counter(), key=lambda x: x[0])])


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        log.warn("missing path argument!")
        log.warn("Usage: python3 main.py $path_to_input $path_to_output $format $converter_type $program")
        pass
    elif len(sys.argv) == 2:
        convert_output_file(path=sys.argv[1])
    elif len(sys.argv) == 3:
        convert_output_file(path=sys.argv[1], out=sys.argv[2])
    elif len(sys.argv) == 4:
        convert_output_file(path=sys.argv[1], out=sys.argv[2], serialization_format=sys.argv[3])
    elif len(sys.argv) == 5:
        convert_output_file(path=sys.argv[1], out=sys.argv[2], serialization_format=sys.argv[3],
                            converter_type=sys.argv[4])
    elif len(sys.argv) > 5:
        convert_output_file(path=sys.argv[1], out=sys.argv[2], serialization_format=sys.argv[3],
                            converter_type=sys.argv[4], program=sys.argv[5])
