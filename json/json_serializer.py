import string

from serializer.json.mappers import *
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
            return self._dumps_dict(set_to_dict(obj))
        elif isinstance(obj, frozenset):
            return self._dumps_dict(frozenset_to_dict(obj))
        elif isinstance(obj, tuple):
            return self._dumps_dict(tuple_to_dict(obj))
        elif isinstance(obj, list):
            return self._dumps_list(obj)
        elif isinstance(obj, dict):
            return self._dumps_dict(obj)
        elif inspect.isfunction(obj):
            res = self._dumps_dict(function_to_dict(obj))
            return res

        elif inspect.isclass(obj):
            return self._dumps_dict(class_to_dict(obj))
        elif is_simple_object(obj):
            return self._dumps_dict(object_to_dict(obj))
        elif isinstance(obj, types.CodeType):
            return self._dumps_dict(code_to_dict(obj))
        elif isinstance(obj, types.CellType):
            return self._dumps_dict(cell_to_dict(obj))
        else:
            raise TypeError()

    def _dumps_list(self, obj):
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

    def _dumps_dict(self, obj):
        if not len(obj):
            return "{}"

        res = "{ "
        keys = list(obj)
        for i in keys[:-1]:
            res += (
                    '"' + str(i) + '": ' + self._dumps(obj[i]) + ", "
            )
        res += (
            f'"{str(keys[-1])}": {self._dumps(obj[keys[-1]])} }}'
        )
        return res

    def dumps(self, obj) -> string:
        return self._dumps(obj)


        """
        elif isinstance(obj, staticmethod):
            res = self._dumps_dict(static_method_to_dict(obj))
            return res
        elif isinstance(obj, classmethod):
            res = self._dumps_dict(class_method_to_dict(obj))
            return res
        """
