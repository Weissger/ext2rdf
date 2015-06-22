from RDFConverter.AbstractConverter import AbstractConverter

__author__ = 'tmy'

from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, URIRef
import urllib.parse as urllib
import logging
import re
from Utilities.Constants import config

log = logging.getLogger()
log.setLevel(config['app']['app_log_level'])

class Converter(AbstractConverter):

    def __init__(self, path):
        self.namespace = Namespace(config['app']['namespace'])
        self.log_file = path

    def convert(self, data_frame):
        pass
