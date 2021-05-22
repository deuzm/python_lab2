import json_serializer.json_serializer

import pytest

from json_serializer.json_serializer import *
from test.utils import *


@pytest.mark.parametrize("test_input, expected",
                         [
                             ({1, 2, 3}, [1, 2, 3]),
                             ({1, "str", 1.4, None}, [1, "str", 1.4, None]),
                             ({}, [])
                         ]
                         )
def test_set_to_dict(test_input, expected):
    result = set_to_dict(test_input)
    assert len(result) == 1
    assert result['set_type'] is not None
    assert compare(result['set_type'], expected)


@pytest.mark.parametrize("test_input, expected",
                         [
                             (frozenset({1, 2, 3}), [1, 2, 3]),
                             (frozenset({1, "str", 1.4, None}), [1, "str", 1.4, None]),
                             (frozenset({}), [])
                         ]
                         )
def test_frozenset_to_dict(test_input, expected):
    result = frozenset_to_dict(test_input)
    assert len(result) == 1
    assert result['frozenset_type'] is not None
    assert compare(result['frozenset_type'], expected)


@pytest.mark.parametrize("test_input, expected",
                         [
                             ((1, 2, 3), (1, 2, 3)),
                             ((1, "str", 1.4, None), (1, "str", 1.4, None)),
                             ((), ())
                         ]
                         )
def test_tuple_to_dict(test_input, expected):
    result = tuple_to_dict(test_input)
    assert len(result) == 1
    assert result['tuple_type'] is not None
    assert compare(result['tuple_type'], expected)


@pytest.mark.parametrize("test_input, expected",
                         [
                             (multiplier(3, 7).__closure__[0], ('n', 'd')),
                         ]
                         )
def test_cell_to_dict(test_input, expected):
    result = cell_to_dict(test_input)
    assert len(result) == 1
    assert result['cell_type'] is not None


@pytest.mark.parametrize("test_input",
                         [
                             TestClass(3, 7).class_m,
                         ]
                         )
def test_class_func(test_input):
    result = class_method_to_dict(test_input)
    assert len(result) == 1
    assert result['class_method_type'] is not None


@pytest.mark.parametrize("test_input",
                         [
                             SimpleClass('a', 3),
                             SimpleClass(None, None)
                         ]
                         )
def test_obj_to_dict(test_input):
    result = object_to_dict(test_input)
    assert len(result) == 1
    assert result['instance_type'] is not None
    assert result['instance_type']['vars'] is not None
    assert compare(result['instance_type']['vars'], test_input.__dict__)


@pytest.mark.parametrize("test_input",
                         [
                             TestClass
                         ]
                         )
def test_class(test_input):
    result = class_to_dict(test_input)
    assert len(result) == 1


@pytest.mark.parametrize("test_input, expected_gls",
                         [
                             (clear_func, 0),
                             (side_func, 2)
                         ]
                         )
def test_gather_gls(test_input, expected_gls):
    result = gather_gls(test_input, test_input.__code__)
    assert len(result) == expected_gls


@pytest.mark.parametrize("module, expected",
                         [
                             (json_serializer.mappers, {'module_type': 'json_serializer.mappers'}),
                         ]
                         )
def test_module_to_dict(module, expected):
    assert module_to_dict(json_serializer.mappers) == expected


@pytest.mark.parametrize("dct",
                         [
                             ({'module_type': 'json_serializer.mappers'}),
                         ]
                         )
def test_module_loads(dct):
    assert dict_to_module(dct)


@pytest.mark.parametrize("dct",
                         [
                             ({'module_type': 'json_serializer.not_exists'}),
                         ]
                         )
def test_module_invalid_path(dct):
    with pytest.raises(ImportError):
        dict_to_module(dct)


def test_collect_functions():
    assert collect_funcs(side_func, {}).keys() == {'compare', 'clear_func', 'multiplier', 'side_func'}


def test_invalid_object():
    with pytest.raises(StopIteration):
        dict_to_obj({})


def test_invalid_cls():
    with pytest.raises(StopIteration):
        dict_to_class({})
