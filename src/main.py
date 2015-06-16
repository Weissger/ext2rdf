__author__ = 'tmy'

from Utilities.Constants import config
from RDFConverter.OpenIEConverter import Converter
from DataParser.parser import DataParser
import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)

def convert_output_file(path, out=config['app']['data_path'] + "output", program=config['app']['program']):
    data_parser = DataParser()
    df = data_parser.parse(program, path)
    rdf_converter = Converter()
    graph = rdf_converter.convert(df)
    graph.serialize(out, "n3")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        log.warn("missing path argument!")
        log.warn("Usage: python3 main.py $path $program")
        pass
    elif len(sys.argv) == 2:
        convert_output_file(path=sys.argv[1])
    elif len(sys.argv) == 3:
        convert_output_file(path=sys.argv[1], out=sys.argv[2])
    elif len(sys.argv) < 3:
        convert_output_file(path=sys.argv[1], out=sys.argv[2], program=sys.argv[3])
