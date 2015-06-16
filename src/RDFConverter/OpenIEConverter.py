from RDFConverter.AbstractConverter import AbstractConverter

__author__ = 'tmy'

from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, URIRef
import urllib.parse as urllib
import logging
import re
from Utilities.Constants import config

log = logging.getLogger()
log.setLevel(logging.DEBUG)

arg_pattern = r'^SimpleArgument\(([0-9]*\s+)?'
list_pattern = r',List\(.*\)$'
relation_pattern = r'^Relation\('
context_pattern = r'^Context\(([0-9]*\s+)?'
temporal_pattern = r'^TemporalArgument\('
spatial_pattern = r'^SpatialArgument\('
arg2s_split_pattern = re.compile('; (' + arg_pattern + '|' + temporal_pattern + '|' + spatial_pattern + ')')


class Converter(AbstractConverter):

    relation = "relation",
    simple = "simple",
    temporal = "temporal",
    spatial = "spatial"

    def __init__(self):
        self.namespace = Namespace(config['app']['namespace'])

    def convert(self, data_frame):
        graph = Graph()
        for _, row in data_frame.iterrows():
            bnode = BNode()
            if 'arg2s' in row and type(row['arg2s']) != float:
                arg2s = re.split(arg2s_split_pattern, row['arg2s'])
                for index, arg in enumerate(arg2s):
                    converted_arg = self.__convert_arg(arg, graph)
                    if index == 0:
                        graph.add((bnode, RDF.object, converted_arg['node']))
                    else:
                        if converted_arg['type'] == Converter.simple:
                            graph.add((bnode, self.namespace.argument, converted_arg['node']))
                        elif converted_arg['type'] == Converter.temporal:
                            graph.add((bnode, self.namespace.temporal, converted_arg['node']))
                        elif converted_arg['type'] == Converter.spatial:
                            graph.add((bnode, self.namespace.spatial, converted_arg['node']))

            elif 'arg2' in row and type(row['arg2']) != float:
                graph.add((bnode, RDF.object, self.__convert_arg(row['arg2'], graph)))
            else:
                pass
            graph.add((bnode, RDF.type, RDF.Statement))
            if 'confidence' in row:
                graph.add((bnode, self.namespace.extraction_confidence, Literal(row['confidence'])))
            if 'context' in row and type(row['context']) != float:
                graph.add((bnode, self.namespace.context, Literal(re.sub(context_pattern + '|' + list_pattern, '', row['context']))))
            graph.add((bnode, RDF.subject, self.__convert_arg(row['arg1'], graph)['node']))
            graph.add((bnode, RDF.predicate, self.__convert_arg(row['rel'], graph)['node']))
        return graph

    def __convert_arg(self, arg, graph):
        if re.match(relation_pattern, arg):
            cleaned_arg = re.sub(relation_pattern + '|' + list_pattern, '', arg)
            url = urllib.quote(cleaned_arg, '')
            node = self.namespace[url]
            graph.add((node, RDF.type, RDF.Property))
            graph.add((node, RDFS.label, Literal(cleaned_arg)))
            return {'type': Converter.relation, 'node': node}
        elif re.match(arg_pattern, arg):
            cleaned_arg = re.sub(arg_pattern + '|' + list_pattern, '', arg)
            url = urllib.quote(cleaned_arg, '')
            node = self.namespace[url]
            graph.add((node, RDFS.label, Literal(cleaned_arg)))
            return {'type': Converter.simple, 'node': node}
        elif re.match(temporal_pattern, arg):
            cleaned_arg = re.sub(temporal_pattern + '|' + list_pattern, '', arg)
            node = Literal(cleaned_arg)
            return {'type': Converter.temporal, 'node': node}
        elif re.match(spatial_pattern, arg):
            cleaned_arg = re.sub(spatial_pattern + '|' + list_pattern, '', arg)
            node = Literal(cleaned_arg)
            return {'type': Converter.spatial, 'node': node}
        else:
            log.warn("For argument: {}".format(arg))
            raise ValueError("tried to convert malformed argument")

