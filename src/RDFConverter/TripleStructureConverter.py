__author__ = 'tmy'

from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, URIRef
import urllib.parse as urllib
import logging
import pandas as pd
from Utilities.Constants import config, SUB_SEPARATOR
from RDFConverter.AbstractConverter import AbstractConverter

log = logging.getLogger()
log.setLevel(config['app']['app_log_level'])


class Converter(AbstractConverter):

    def __init__(self):
        self.namespace = Namespace(config['app']['namespace'])

    def convert(self, data_frame):
        log.info("converting data_frame...")
        graph = Graph()
        for _, row in data_frame.iterrows():

            # Subject
            subject_uri = urllib.quote(row['Subject'], '')
            subject_node = URIRef(self.namespace[subject_uri])
            graph.add((subject_node, RDFS.label, Literal(row['Subject'])))

            # Predicate
            predicate_uri = urllib.quote(row['Predicate'], '')
            predicate_node = URIRef(self.namespace[predicate_uri])
            graph.add((predicate_node, RDFS.label, Literal(row['Predicate'])))

            # Object
            object_uri = urllib.quote(row['Object'], '')
            object_node = URIRef(self.namespace[object_uri])
            graph.add((object_node, RDFS.label, Literal(row['Object'])))

            graph.add((subject_node, predicate_node, object_node))

            # Predicate Lemmatized
            if not pd.isnull(row['PredicateLemma']):
                predicate_lemma_uri = urllib.quote(row['PredicateLemma'], '')
                predicate_lemma_node = URIRef(self.namespace[predicate_lemma_uri])
                graph.add((subject_node, predicate_lemma_node, object_node))

        return graph
