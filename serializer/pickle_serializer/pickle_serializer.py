import pickle

import string

from basic_serializer import Serializer
from serializer.test.utils import TestClass


class PickleSerializer(Serializer):

    def dump(self, obj, filename: string):
        return pickle.dump(obj, open(filename, "wb"))

    def dumps(self, obj) -> string:
        return pickle.dumps(obj)

    def load(self, filename: string):
        return pickle.load(open(filename, 'rb'))

    def loads(self, data: string):
        return pickle.loads(data)

