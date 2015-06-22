from RDFConverter.AbstractConverter import AbstractConverter

__author__ = 'tmy'

from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, URIRef
import urllib.parse as urllib
import logging
import re
from Utilities.Constants import config

log = logging.getLogger()
log.setLevel(config['app']['app_log_level'])

arg_pattern = r'^SimpleArgument\(([0-9]*\s+)?'
list_pattern = r',List\(.*\)$'
relation_pattern = r'^Relation\('
context_pattern = r'^Context\(([0-9]*\s+)?'
temporal_pattern = r'^TemporalArgument\('
spatial_pattern = r'^SpatialArgument\('
arg2s_split_pattern = r'; (SimpleArgument|TemporalArgument|SpatialArgument)'


class Converter(AbstractConverter):

    relation = "relation",
    simple = "simple",
    temporal = "temporal",
    spatial = "spatial"

    def __init__(self, path):
        self.namespace = Namespace(config['app']['namespace'])
        self.log_file = path + ".rl"

    def convert(self, data_frame):
        read_list_file = open(self.log_file, "w+")
        log.info("converting data_frame...")
        graph = Graph()
        for _, row in data_frame.iterrows():
            bnode = BNode()
            line = []
            if 'arg2s' in row and type(row['arg2s']) != float:
                arg2s = re.split(arg2s_split_pattern, row['arg2s'])
                for index, arg in enumerate(arg2s):
                    if arg == "SimpleArgument" or arg == "TemporalArgument" or arg == "SpatialArgument":
                        arg2s[index + 1] = arg + arg2s[index + 1]
                    else:
                        converted_arg = self.__convert_arg(arg, graph)
                        if index == 0:
                            line.append(converted_arg['cleaned_arg'])
                            graph.add((bnode, RDF.object, converted_arg['node']))
                        else:
                            if converted_arg['type'] == Converter.simple:
                                line.append("Arg: " + converted_arg['cleaned_arg'])
                                graph.add((bnode, self.namespace.argument, converted_arg['node']))
                            elif converted_arg['type'] == Converter.temporal:
                                line.append("Temp: " + converted_arg['cleaned_arg'])
                                graph.add((bnode, self.namespace.temporal, converted_arg['node']))
                            elif converted_arg['type'] == Converter.spatial:
                                line.append("Spatial: " + converted_arg['cleaned_arg'])
                                graph.add((bnode, self.namespace.spatial, converted_arg['node']))

            elif 'arg2' in row and type(row['arg2']) != float:
                converted_arg = self.__convert_arg(row['arg2'], graph)
                line.append(converted_arg['cleaned_arg'])
                graph.add((bnode, RDF.object, converted_arg['node']))
            else:
                pass
            graph.add((bnode, RDF.type, RDF.Statement))
            converted_pred = self.__convert_arg(row['rel'], graph)
            graph.add((bnode, RDF.predicate, converted_pred['node']))
            line.insert(0, converted_pred['cleaned_arg'])
            converted_sub = self.__convert_arg(row['arg1'], graph)
            graph.add((bnode, RDF.subject, converted_sub['node']))
            line.insert(0, converted_sub['cleaned_arg'])
            if 'context' in row and type(row['context']) != float:
                context = re.sub(context_pattern + '|' + list_pattern, '', row['context'])
                line.insert(0, context)
                graph.add((bnode, self.namespace.context, Literal(context)))
            else:
                line.insert(0, "")
            line.insert(0, "{0:.2f}".format(row['confidence']))
            graph.add((bnode, self.namespace.extraction_confidence, Literal(row['confidence'])))

            read_list_file.write("\t".join(line) + "\n")
        read_list_file.close()
        return graph

    def __convert_arg(self, arg, graph):
        if re.match(relation_pattern, arg):
            cleaned_arg = re.sub(relation_pattern + '|' + list_pattern, '', arg)
            url = urllib.quote(cleaned_arg, '')
            node = self.namespace[url]
            graph.add((node, RDF.type, RDF.Property))
            graph.add((node, RDFS.label, Literal(cleaned_arg)))
            return {'type': Converter.relation, 'node': node, 'cleaned_arg': cleaned_arg}
        elif re.match(arg_pattern, arg):
            cleaned_arg = re.sub(arg_pattern + '|' + list_pattern, '', arg)
            url = urllib.quote(cleaned_arg, '')
            node = self.namespace[url]
            graph.add((node, RDFS.label, Literal(cleaned_arg)))
            return {'type': Converter.simple, 'node': node, 'cleaned_arg': cleaned_arg}
        elif re.match(temporal_pattern, arg):
            cleaned_arg = re.sub(temporal_pattern + '|' + list_pattern, '', arg)
            node = Literal(cleaned_arg)
            return {'type': Converter.temporal, 'node': node, 'cleaned_arg': cleaned_arg}
        elif re.match(spatial_pattern, arg):
            cleaned_arg = re.sub(spatial_pattern + '|' + list_pattern, '', arg)
            node = Literal(cleaned_arg)
            return {'type': Converter.spatial, 'node': node, 'cleaned_arg': cleaned_arg}
        else:
            log.warn("For argument: {}".format(arg))
            raise ValueError("tried to convert malformed argument")

