__author__ = 'tmy'

from Utilities.Constants import sub_separator, separator
import numpy as np


class Extraction():
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
        line = [self.confidence, self.context, self.subject, self.predicate, self.object,
                sub_separator.join(self.additional_args),
                sub_separator.join(self.temporal_args), sub_separator.join(self.spatial_args), self.sentence_id,
                self.sentence]
        return separator.join(line)