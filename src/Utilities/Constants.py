__author__ = 'tmy'

from enum import Enum


class PROGRAMS(Enum):
    OPENIE = 'OpenIE'
    REVERB = 'Reverb'


ARG_TYPES = {
    'rel': "relation",
    'simple': "simple",
    'tmp': "temporal",
    'spatial': "spatial"
}

CONVERTER_TYPES = {
    'reification': "reification",
    'triple': "triple",
    'simple': "simple"
}

SEPARATOR = '\t'
SUB_SEPARATOR = ' | '

E2RDF_COLUMN_NAMES = ["Confidence", "Context", "Subject", "Predicate", "PredicateLemma", "Object", "Other_arg",
                      "Temporal", "Spatial",
                      "Sentence_id", "Sentence"]

MAX_LENGTHS = {
    'subject': 0,
    'predicate': 0,
    'object': 0
}


NAMESPACE = 'http://QA.jbt.org/'

import logging
LOG_LEVEL = logging.DEBUG
