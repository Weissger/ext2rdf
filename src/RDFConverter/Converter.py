__author__ = 'tmy'

from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, URIRef
import urllib.parse as urllib
import logging
import pandas as pd
from Utilities.Constants import config, sub_separator

log = logging.getLogger()
log.setLevel(config['app']['app_log_level'])


class Converter(object):

    def __init__(self):
        self.namespace = Namespace(config['app']['namespace'])

    def convert(self, data_frame):
        log.info("converting data_frame...")
        graph = Graph()
        for _, row in data_frame.iterrows():
            bnode = BNode()
            # Confidence
            if not pd.isnull(row['Confidence']):
                graph.add((bnode, self.namespace.extraction_confidence, Literal(row['Confidence'])))
            # Context
            if not pd.isnull(row['Context']):
                graph.add((bnode, self.namespace.context, Literal(row['Context'])))
            # Subject
            uri = urllib.quote(row['Subject'], '')
            node = URIRef(uri)
            graph.add((bnode, RDF.subject, node))
            graph.add((node, RDFS.label, Literal(row['Subject'])))
            # Predicate
            uri = urllib.quote(row['Predicate'], '')
            node = URIRef(uri)
            graph.add((bnode, RDF.predicate, node))
            graph.add((node, RDFS.label, Literal(row['Predicate'])))
            # Object
            uri = urllib.quote(row['Object'], '')
            node = URIRef(uri)
            graph.add((bnode, RDF.object, node))
            graph.add((node, RDFS.label, Literal(row['Object'])))
            # Additional Args
            if not pd.isnull(row['Other_arg']):
                for arg in row['Other_arg'].split(sub_separator):
                    uri = urllib.quote(arg, '')
                    node = URIRef(uri)
                    graph.add((bnode, self.namespace.argument, node))
                    graph.add((node, RDFS.label, Literal(arg)))
            # Temporal
            if not pd.isnull(row['Temporal']):
                for arg in row['Temporal'].split(sub_separator):
                    graph.add((bnode, self.namespace.temporal, Literal(arg)))
            # Spatial
            if not pd.isnull(row['Spatial']):
                for arg in row['Spatial'].split(sub_separator):
                    uri = urllib.quote(arg, '')
                    node = URIRef(uri)
                    graph.add((bnode, self.namespace.spatial, node))
                    graph.add((node, RDFS.label, Literal(arg)))
        return graph