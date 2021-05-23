from serializer.json_serializer.mappers import *

sort_keys = False

def parse_digit(string, idx):
    first = idx
    try:
        while (
                string[idx] == "."
                or string[idx].isdigit()
                or string[idx] == "e"
                or string[idx] == "E"
                or string[idx] == "-"
                or string[idx] == "+"
        ):
            idx += 1
    except IndexError:
        pass
    res = string[first:idx]
    try:
        return int(res), idx
    except ValueError:
        try:
            return float(res), idx
        except ValueError:
            raise StopIteration(idx)


def parse_list(string, idx):
    args = []
    comma = False

    try:
        next_char = string[idx]
    except IndexError:
        raise StopIteration(idx)
    while True:
        if next_char == "]":
            break
        elif next_char == " " or next_char == "\n":
            idx += 1
        elif next_char == ",":
            if comma is False:
                raise StopIteration(idx)
            idx += 1
            comma = False
        elif not comma:
            obj, idx = parse_symbol(string, idx)
            args.append(obj)

            comma = True
        else:
            raise StopIteration(idx)
        try:
            next_char = string[idx]
        except IndexError:
            raise StopIteration(idx)
    if not comma and len(args) != 0:
        raise StopIteration(idx)
    return list(args), idx + 1


def parse_symbol(string, idx):
    if string[idx] == '"':
        obj, idx = parse_string(string, idx + 1)
    elif string[idx].isdigit() or (string[idx] == "-" and string[idx + 1].isdigit()):
        obj, idx = parse_digit(string, idx)
    elif string[idx] == "{":
        obj, idx = parse_dict(string, idx + 1)
    elif string[idx] == "[":
        obj, idx = parse_list(string, idx + 1)
    elif string[idx] == "n" and string[idx: idx + 4] == "null":
        obj = None
        idx += 4
    elif string[idx] == "t" and string[idx: idx + 4] == "true":
        obj = True
        idx += 4
    elif string[idx] == "f" and string[idx: idx + 5] == "false":
        obj = False
        idx += 5
    elif string[idx] == "n" and string[idx: idx + 3] == "nan":
        obj = float("NaN")
        idx += 3
    elif string[idx] == "i" and string[idx: idx + 3] == "inf":
        obj = float("Infinity")
        idx += 3
    elif string[idx] == "-" and string[idx: idx + 4] == "-inf":
        obj = float("-Infinity")
        idx += 4
    else:
        raise StopIteration(idx)
    return obj, idx


def parse_dict(string, idx):
    args = {}
    comma = False
    colon = False
    phase = False
    temp = None

    try:
        next_char = string[idx]
    except IndexError:
        raise StopIteration(idx)
    while True:
        if next_char == "}":
            break
        elif next_char == " " or next_char == "\n":
            idx += 1
        elif next_char == ",":
            if comma is False:
                raise StopIteration(idx)
            idx += 1
            phase = False
            comma = False
        elif next_char == ":":
            if colon is False:
                raise StopIteration(idx)
            idx += 1
            phase = True
            colon = False
        elif not comma and not phase:
            if next_char == '"':
                obj, idx = parse_string(string, idx + 1)
                if obj in args:
                    raise StopIteration(idx)
                temp = obj
                phase = False
                colon = True
            else:
                raise StopIteration(idx)
        elif not colon and phase:
            obj, idx = parse_symbol(string, idx)
            args[temp] = obj

            comma = True
        else:
            raise StopIteration(idx)
        try:
            next_char = string[idx]
        except IndexError:
            raise StopIteration(idx)

    if not comma and not colon and len(args) != 0:
        raise StopIteration(idx)
    if "function_type" in args and len(args.keys()) == 1:
        return dict_to_func(args["function_type"]), idx + 1
    if "static_method_type" in args and len(args.keys()) == 1:
        return staticmethod(args["static_method_type"]), idx + 1
    if "class_method_type" in args and len(args.keys()) == 1:
        return classmethod(args["class_method_type"]), idx + 1
    if "class_type" in args and len(args.keys()) == 1:
        return dict_to_class(args["class_type"]), idx + 1
    if "instance_type" in args and len(args.keys()) == 1:
        return dict_to_obj(args["instance_type"]), idx + 1
    if "module_type" in args and len(args.keys()) == 1:
        return dict_to_module(args["module_type"]), idx + 1
    if "code_type" in args and len(args.keys()) == 1:
        return parse_code(args["code_type"]), idx + 1
    if "cell_type" in args and len(args.keys()) == 1:
        return dict_to_cell(args["cell_type"]), idx + 1
    if "tuple_type" in args and len(args.keys()) == 1:
        return tuple(args["tuple_type"]), idx + 1
    if "frozenset_type" in args and len(args.keys()) == 1:
        return frozenset(args["frozenset_type"]), idx + 1
    if "set_type" in args and len(args.keys()) == 1:
        return set(args["set_type"]), idx + 1
    else:
        if sort_keys:
            return dict(sorted(args.items())), idx + 1
        else:
            return args, idx + 1


def parse_string(string, idx):
    first = idx
    opened = False
    try:
        while string[idx] != '"' or opened:
            if string[idx] == "\\":
                opened = not opened
            else:
                opened = False
            idx += 1
    except IndexError:
        raise StopIteration(idx)
    return string[first:idx], idx + 1


def parse_code(obj):
    return types.CodeType(
        obj["co_argcount"],
        obj["co_posonlyargcount"],
        obj["co_kwonlyargcount"],
        obj["co_nlocals"],
        obj["co_stacksize"],
        obj["co_flags"],
        bytes(bytearray(parse_list(obj["co_code"], 1)[0])),
        obj["co_consts"],
        obj["co_names"],
        obj["co_varnames"],
        obj["co_filename"],
        obj["co_name"],
        obj["co_firstlineno"],
        bytes(bytearray(parse_list(obj["co_lnotab"], 1)[0])),
        obj["co_freevars"],
        obj["co_cellvars"],
    )