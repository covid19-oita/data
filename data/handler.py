from abc import ABCMeta
from abc import abstractmethod


class Handler(metaclass=ABCMeta):
    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def convert(self):
        pass

    @abstractmethod
    def write(self):
        pass


class classname(object):
    pass
