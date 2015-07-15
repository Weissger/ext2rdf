#!/usr/bin/env python3

__author__ = 'tmy'

from ext2rdf.src.Utilities.Constants import LOG_LEVEL, PROGRAMS, E2RDF_COLUMN_NAMES, SEPARATOR, CONVERTER_TYPES, MAX_LENGTHS
from ext2rdf.src.DataParser import OpenIEParser
from ext2rdf.src.DataParser import ReverbParser
from ext2rdf.src.RDFConverter import ReificationStructureConverter
from ext2rdf.src.RDFConverter import TripleStructureConverter
from ext2rdf.src.RDFConverter import SimpleStructureConverter
import csv
import pandas as pd
import logging
from io import StringIO

log = logging.getLogger()
log.setLevel(LOG_LEVEL)


def generate_e2rdf(extractions):
    s = StringIO("\n".join([e.to_e2rdf() for e in extractions]))
    return pd.read_csv(s, names=E2RDF_COLUMN_NAMES, sep=SEPARATOR, quoting=csv.QUOTE_NONE)


def write_to_disk(path, dataframe):
    filename = path + ".e2rdf"

    with open(filename, 'w', encoding='utf-8') as _:
        pass
    with open(filename, 'a', encoding='utf-8') as f:
        for _, row in dataframe.iterrows():
            f.write(SEPARATOR.join(row.map(str)) + "\n")


def convert_output_file(input_file, output_file="output", serialization_format="nt", converter_type=CONVERTER_TYPES['reification'], program=PROGRAMS.OPENIE):
    if program is PROGRAMS.OPENIE:
        data_parser = OpenIEParser.DataParser()
    elif program is PROGRAMS.REVERB:
        data_parser = ReverbParser.DataParser()
    else:
        log.warn("Unknown program")
        return
    extractions = data_parser.parse(input_file)
    df = generate_e2rdf(extractions)

    # Subject length filter
    max_len = MAX_LENGTHS['subject']
    if max_len > 0:
        df = df[df['Subject'].map(str.split, " ").map(len) <= max_len]

    # Predicate length filter
    max_len = MAX_LENGTHS['predicate']
    if max_len > 0:
        df = df[df['Predicate'].map(str.split, " ").map(len) <= max_len]

    # Object length filter
    max_len = MAX_LENGTHS['object']
    if max_len > 0:
        df = df[df['Object'].map(str.split, " ").map(len) <= max_len]

    write_to_disk(output_file, df)

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
    graph.serialize(output_file + "." + serialization_format, serialization_format)

    log.warn([(e, data_parser.get_counter()[e]) for e in sorted(data_parser.get_counter(), key=lambda x: x[0])])


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        log.warn("missing path argument!")
        log.warn("Usage: python3 main.py $path_to_input $path_to_output $format $converter_type $program")
        pass
    elif len(sys.argv) == 2:
        convert_output_file(input_file=sys.argv[1])
    elif len(sys.argv) == 3:
        convert_output_file(input_file=sys.argv[1], output_file=sys.argv[2])
    elif len(sys.argv) == 4:
        convert_output_file(input_file=sys.argv[1], output_file=sys.argv[2], serialization_format=sys.argv[3])
    elif len(sys.argv) == 5:
        convert_output_file(input_file=sys.argv[1], output_file=sys.argv[2], serialization_format=sys.argv[3],
                            converter_type=sys.argv[4])
    elif len(sys.argv) > 5:
        convert_output_file(input_file=sys.argv[1], output_file=sys.argv[2], serialization_format=sys.argv[3],
                            converter_type=sys.argv[4], program=sys.argv[5])
