__author__ = 'tmy'

from Utilities.Constants import config, programs
from RDFConverter import OpenIEConverter
from RDFConverter import ReverbConverter
from DataParser.parser import DataParser
import logging

log = logging.getLogger()
log.setLevel(config['app']['app_log_level'])

def convert_output_file(path, out=config['app']['data_path'] + "output", ser_format="nt", program=config['app']['program']):
    data_parser = DataParser()
    df = data_parser.parse(program, path)
    if program == programs['oIE']:
        rdf_converter = OpenIEConverter.Converter(out)
    elif program == programs['rvb']:
        rdf_converter = OpenIEConverter.Converter(out)
    else:
        log.warn("Unknown program")
        return
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
