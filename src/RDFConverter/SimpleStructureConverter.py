__author__ = 'tmy'

from rdflib import Graph, Namespace, URIRef
import urllib.parse as urllib
import logging
from ext2rdf.src.Utilities.Constants import LOG_LEVEL, NAMESPACE
from ext2rdf.src.RDFConverter.AbstractConverter import AbstractConverter

log = logging.getLogger()
log.setLevel(LOG_LEVEL)


class Converter(AbstractConverter):

    def __init__(self):
        self.namespace = Namespace(NAMESPACE)

    def convert(self, data_frame):
        log.info("converting data_frame...")
        graph = Graph()
        for _, row in data_frame.iterrows():

            # Subject
            subject_uri = urllib.quote(row['Subject'], '')
            subject_node = URIRef(self.namespace[subject_uri])

            # Predicate
            predicate_uri = urllib.quote(row['Predicate'], '')
            predicate_node = URIRef(self.namespace[predicate_uri])

            # Object
            object_uri = urllib.quote(row['Object'], '')
            object_node = URIRef(self.namespace[object_uri])

            graph.add((subject_node, predicate_node, object_node))

        return graph
