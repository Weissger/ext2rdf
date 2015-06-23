__author__ = 'tmy'

from Utilities.Constants import SUB_SEPARATOR, SEPARATOR
import numpy as np


class Extraction(object):
    def __init__(self, data):
        self.subject = data['subject']
        self.predicate = data['predicate']
        self.object = data['object']
        self.context = data['context'] if 'context' in data else np.nan
        self.confidence = str(data['confidence']) if 'confidence' in data else np.nan
        self.additional_args = data['additional_args'] if 'additional_args' in data else np.nan
        self.temporal_args = data['temporal_args'] if 'temporal_args' in data else np.nan
        self.spatial_args = data['spatial_args'] if 'spatial_args' in data else np.nan
        self.sentence_id = str(data['sentence_id'])
        self.sentence = data['sentence']

    def to_e2rdf(self):
        return SEPARATOR.join(
            [self.confidence, self.context, self.subject, self.predicate, self.object,
             SUB_SEPARATOR.join(self.additional_args),
             SUB_SEPARATOR.join(self.temporal_args), SUB_SEPARATOR.join(self.spatial_args), self.sentence_id,
             self.sentence])
