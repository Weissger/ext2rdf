__author__ = 'tmy'

import abc


class AbstractParser(object):
    """
    Abstract class to implement a parser.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def parse(self, path):
        pass

    @abc.abstractmethod
    def get_counter(self):
        pass
