__author__ = 'tmy'

from Utilities.Constants import config, programs, e2rdf_cols, separator
from DataParser import OpenIEParser
from DataParser import ReverbParser
from RDFConverter.Converter import Converter
import csv
import pandas as pd
import logging

log = logging.getLogger()
log.setLevel(config['app']['app_log_level'])


def generate_e2rdf(path, extractions):
    with open(path + ".e2rdf", "w") as _:
        pass
    with open(path + ".e2rdf", "a") as f:
        for ext in extractions:
            f.write(ext.to_e2rdf() + "\n")
        f.close()
    return pd.read_csv(path + ".e2rdf", names=e2rdf_cols, sep=separator, quoting=csv.QUOTE_NONE)


def convert_output_file(path, out=config['app']['data_path'] + "output", ser_format="nt",
                        program=config['app']['program']):
    if program == programs['oIE']:
        data_parser = OpenIEParser.DataParser()
    elif program == programs['rvb']:
        data_parser = ReverbParser.DataParser()
    else:
        log.warn("Unknown program")
        return
    extractions = data_parser.parse(path)
    df = generate_e2rdf(out, extractions)

    # Subject length filter
    max_len = int(config['app']['max_subject_length'])
    if max_len > 0:
        df = df[df['Subject'].map(len) <= max_len]

    # Predicate length filter
    max_len = int(config['app']['max_predicate_length'])
    if max_len > 0:
        df = df[df['Predicate'].map(len) <= max_len]
    max_len = int(config['app']['max_object_length'])

    # Object length filter
    if max_len > 0:
        df = df[df['Object'].map(len) <= max_len]
    rdf_converter = Converter()
    graph = rdf_converter.convert(df)
    graph.serialize(out + "." + ser_format, ser_format)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        log.warn("missing path argument!")
        log.warn("Usage: python3 main.py $path_to_input $path_to_output $format $program")
        pass
    elif len(sys.argv) == 2:
        convert_output_file(path=sys.argv[1])
    elif len(sys.argv) == 3:
        convert_output_file(path=sys.argv[1], out=sys.argv[2])
    elif len(sys.argv) == 4:
        convert_output_file(path=sys.argv[1], out=sys.argv[2], ser_format=sys.argv[3])
    elif len(sys.argv) < 4:
        convert_output_file(path=sys.argv[1], out=sys.argv[2], ser_format=sys.argv[3], program=sys.argv[4])
