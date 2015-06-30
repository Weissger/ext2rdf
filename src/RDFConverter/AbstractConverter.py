__author__ = 'tmy'

import abc


class AbstractConverter(object):
    """
    Abstract class to implement a converter.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def convert(self, path):
        pass
