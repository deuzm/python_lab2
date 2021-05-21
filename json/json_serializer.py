import string

from mappers import *
from serializer.basic_serializer import Serializer

f_found = {}


class JsonSerializer(Serializer):

    def _dumps(self, obj):

        if obj is None:
            return "null"
        elif obj is True:
            return "true"
        elif obj is False:
            return "false"
        elif obj is float("Inf"):
            return "Infinity"
        elif obj is float("-Inf"):
            return "-Infinity"
        elif obj is float("NaN"):
            return "NaN"
        elif isinstance(obj, (int, float)):
            return str(obj)
        elif isinstance(obj, bytes):
            return '"' + str(list(bytearray(obj))) + '"'
        elif isinstance(obj, str):
            return '"' + obj.replace("\\", "\\\\").replace('"', '\\"') + '"'
        elif isinstance(obj, set):
            return self.dumps_dict(set_to_dict(obj))
        elif isinstance(obj, frozenset):
            return self.dumps_dict(frozenset_to_dict(obj))
        elif isinstance(obj, tuple):
            return self.dumps_dict(tuple_to_dict(obj))
        elif isinstance(obj, list):
            return self.dumps_list(obj)
        elif isinstance(obj, dict):
            return self.dumps_dict(obj)
        elif inspect.isfunction(obj):
            res = self.dumps_dict(function_to_dict(obj))
            return res
        elif isinstance(obj, staticmethod):
            res = self.dumps_dict(static_method_to_dict(obj))
            return res
        elif isinstance(obj, classmethod):
            res = self.dumps_dict(class_method_to_dict(obj))
            return res
        elif inspect.isclass(obj):
            return self.dumps_dict(class_to_dict(obj))
        elif is_simple_object(obj):
            return self.dumps_dict(object_to_dict(obj))
        elif isinstance(obj, types.CodeType):
            return self.dumps_dict(code_to_dict(obj))
        elif isinstance(obj, types.CellType):
            return self.dumps_dict(cell_to_dict(obj))
        else:
            raise TypeError()

    def dumps_list(self, obj):
        if not len(obj):
            return "[]"
        res = "["
        for i in range(len(obj) - 1):
            res += (
                    self._dumps(obj[i])
                    + ","

            )
        res += (
                self._dumps(obj[-1]) + "]"
        )
        return res

    def dumps_dict(self, obj):
        if not len(obj):
            return "{}"

        res = "{"
        keys = list(obj)
        for i in keys[:-1]:
            res += (
                    '"' + str(i) + '": ' + self._dumps(obj[i]) + ","
            )
        res += (
            f'"{str(keys[-1])}": {self._dumps(obj[keys[-1]])} }}'
        )
        return res

    def dumps(self, obj) -> string:
        return self._dumps(obj)


class PPP:
    def __init__(self):
        self.i = 8

    def kokoko(self, buka):
        print(buka + "LIZA")
        self.i += 3
        return self.i


LIZA = JsonSerializer()
print(LIZA.dumps(PPP))
