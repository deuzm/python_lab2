import string
from abc import abstractmethod


class Serializer:

    @abstractmethod
    def dump(self, obj, filename: string):
        pass

    @abstractmethod
    def dumps(self, obj) -> string:
        pass

    @abstractmethod
    def load(self, filename: string):
        pass

    @abstractmethod
    def loads(self, date: string):
        pass

