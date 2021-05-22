import inspect
import types

BUILTIN_TYPES = (
                    set,
                    dict,
                    list,
                    int,
                    float,
                    bool,
                    type(None),
                    tuple,
                    str
                ),


def set_to_dict(obj):
    return {"set_type": list(obj)}


def frozenset_to_dict(obj):
    return {"frozenset_type": list(obj)}


def tuple_to_dict(obj):
    return {"tuple_type": list(obj)}


def cell_to_dict(obj):
    return {"cell_type": obj.cell_contents}


def is_simple_object(obj):
    return hasattr(obj, "__dict__") and not inspect.isroutine(obj) and not inspect.isclass(obj)


def static_method_to_dict(obj):
    return {"static_method_type": function_to_dict(obj.__func__)}


def class_method_to_dict(obj):
    return {"class_method_type": function_to_dict(obj.__func__)}


def module_to_dict(obj):
    return {"module_type": obj.__name__}


def object_to_dict(obj):
    return {
        "instance_type": {
            "class": class_to_dict(obj.__class__),
            "vars": obj.__dict__,
        }
    }


def function_to_dict(obj):
    gls = gather_gls(obj, obj.__code__)

    return {
        "function_type": {
            "__globals__": gls,
            "__name__": obj.__name__,
            "__code__": code_to_dict(obj.__code__),
            "__defaults__": obj.__defaults__,
            "__closure__": obj.__closure__,
        }
    }


def map_parent_classes(cls):
    parent_classes = ()
    if len(cls.__bases__) != 0:
        for parent_class in cls.__bases__:
            if parent_class.__name__ != "object":
                parent_classes += (class_to_dict(parent_class),)
    return parent_classes


def class_to_dict(cls):
    parent_classes = map_parent_classes(cls)
    global f_found
    args = {}
    st_args = dict(cls.__dict__)
    if len(st_args) != 0:
        for i in st_args:
            if inspect.isclass(st_args[i]):
                args[i] = class_to_dict(st_args[i])
            elif inspect.isfunction(st_args[i]):
                if st_args[i] not in f_found:
                    args[i] = function_to_dict(st_args[i])
            elif isinstance(st_args[i], staticmethod):
                if st_args[i].__func__ not in f_found:
                    args[i] = static_method_to_dict(st_args[i])
            elif isinstance(st_args[i], classmethod):
                if st_args[i].__func__ not in f_found:
                    args[i] = class_method_to_dict(st_args[i])
            elif inspect.ismodule(st_args[i]):
                args[i] = module_to_dict(st_args[i])
            elif is_simple_object(st_args[i]):
                args[i] = object_to_dict(st_args[i])
            elif isinstance(st_args[i], BUILTIN_TYPES):
                args[i] = st_args[i]

    return {"class_type": {"name": cls.__name__, "bases": parent_classes, "dict": args}}


def code_to_dict(obj):
    return {
        "code_type": {
            "co_argcount": obj.co_argcount,
            "co_posonlyargcount": obj.co_posonlyargcount,
            "co_kwonlyargcount": obj.co_kwonlyargcount,
            "co_nlocals": obj.co_nlocals,
            "co_stacksize": obj.co_stacksize,
            "co_flags": obj.co_flags,
            "co_code": obj.co_code,
            "co_consts": obj.co_consts,
            "co_names": obj.co_names,
            "co_varnames": obj.co_varnames,
            "co_filename": obj.co_filename,
            "co_name": obj.co_name,
            "co_firstlineno": obj.co_firstlineno,
            "co_lnotab": obj.co_lnotab,
            "co_freevars": obj.co_freevars,
            "co_cellvars": obj.co_cellvars,
        }
    }


f_found = {}


def gather_gls(obj, obj_code):
    global f_found
    f_found[obj] = True
    vars_global = {}
    for var in obj_code.co_names:
        try:
            if inspect.isclass(obj.__globals__[var]):
                vars_global[var] = class_to_dict(obj.__globals__[var])

            elif inspect.isfunction(obj.__globals__[var]):
                if obj.__globals__[var] not in f_found:
                    vars_global[var] = function_to_dict(obj.__globals__[var])
            elif isinstance(obj.__globals__[var], staticmethod):
                if obj.__globals__[var].__func__ not in f_found:
                    vars_global[var] = static_method_to_dict(obj.__globals__[var])
            elif isinstance(obj.__globals__[var], classmethod):
                if obj.__globals__[var].__func__ not in f_found:
                    vars_global[var] = class_method_to_dict(obj.__globals__[var])
            elif inspect.ismodule(obj.__globals__[var]):
                vars_global[var] = module_to_dict(obj.__globals__[var])
            elif is_simple_object(obj.__globals__[var]):
                vars_global[var] = object_to_dict(obj.__globals__[var])
            elif isinstance(obj.__globals__[var], BUILTIN_TYPES):
                vars_global[var] = obj.__globals__[var]

        except KeyError:
            pass

    for var in obj_code.co_consts:
        if isinstance(var, types.CodeType):
            vars_global.update(gather_gls(obj, var))
    return vars_global


def dict_to_class(cls):
    try:
        return type(cls["name"], cls["bases"], cls["dict"])
    except (IndexError, KeyError):
        raise StopIteration("Incorrect class")


def dict_to_obj(obj):
    try:

        def __init__(self):
            pass

        cls = obj["class"]
        temp = cls.__init__
        cls.__init__ = __init__
        res = obj["class"]()
        res.__dict__ = obj["vars"]
        res.__init__ = temp
        res.__class__.__init__ = temp
        return res
    except (IndexError, KeyError):
        raise StopIteration("Incorrect object")


def dict_to_cell(obj):
    return types.CellType(obj)


def collect_funcs(obj, is_visited):
    for i in obj.__globals__:
        attr = obj.__globals__[i]
        if inspect.isfunction(attr) and attr.__name__ not in is_visited:
            is_visited[attr.__name__] = attr
            is_visited = collect_funcs(attr, is_visited)
    return is_visited


def set_funcs(obj, is_visited, gls):
    for i in obj.__globals__:
        attr = obj.__globals__[i]
        if inspect.isfunction(attr) and attr.__name__ not in is_visited:
            is_visited[attr.__name__] = True
            attr.__globals__.update(gls)
            is_visited = set_funcs(attr, is_visited, gls)
    return is_visited


def dict_to_func(obj):
    closure = None
    if obj["__closure__"] is not None:
        closure = obj["__closure__"]
    res = types.FunctionType(
        globals=obj["__globals__"],
        code=obj["__code__"],
        name=obj["__name__"],
        closure=closure,
    )

    setattr(res, "__defaults__", obj["__defaults__"])

    funcs = collect_funcs(res, {})
    funcs.update({res.__name__: res})
    set_funcs(res, {res.__name__: True}, funcs)
    res.__globals__.update(funcs)
    res.__globals__["__builtins__"] = __import__("builtins")
    return res


def dict_to_module(obj):
    try:
        return __import__(obj['module_type'])
    except ModuleNotFoundError:
        raise ImportError(str(obj) + " not found")
