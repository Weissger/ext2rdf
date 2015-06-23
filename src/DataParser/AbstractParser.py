__author__ = 'tmy'

import abc


class AbstractParser(object):
    """
    Abstract class to implement a converter.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def parse(self, path):
        pass


