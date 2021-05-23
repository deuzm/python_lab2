import pytest

from serializer.json_serializer.json_serializer import JsonSerializer
from serializer.json_serializer.parsers import parse_digit, parse_list, parse_dict
from serializer.test.utils import *


@pytest.mark.parametrize(
    'obj, expected',
    [
        (
                {
                    "number": 3,
                    "float_number": 4.3,
                    "nul": None,
                    "str": "test",
                    "tuple": tuple((1, 3, 7)),
                    "set": {1, 4, 5},
                    "empty": {},
                    "empty_t": tuple(()),
                    "bool": True,
                    "bool2": False,
                    "flt_inf": float("Inf"),
                    "flt_inf2": float("-Inf"),
                    "flt_nan": float("NaN"),
                },
                'serializer/test/output/1.json'
        )
    ]
)
def test_with_pattern(obj, expected):
    f = open(expected)
    result = f.read()
    result = result.replace('/', r'\\')
    assert JsonSerializer().dumps(
        obj
    ).replace(" ", "") == result.replace(" ", "")


@pytest.mark.parametrize(
    "obj",
    [
        {
            "number": 3,
            "float_number": 4.3,
            "nul": None,
            "str": "test",
            "tuple": tuple((1, 3, 7)),
            "set": {1, 4, 5},
            "empty": {},
            "empty_t": tuple(()),
            "bool": True,
            "bool2": False,
            "flt_inf": float("Inf"),
            "flt_inf2": float("-Inf")
        },
        TestClass(3, 7)
    ]
)
def test_serializer(obj):
    json_serializer = JsonSerializer()
    result = json_serializer.loads(json_serializer.dumps(obj))
    if hasattr(result, '__dict__'):
        for x in obj.__dict__:
            assert x in result.__dict__
    else:
        assert obj == json_serializer.loads(json_serializer.dumps(obj))


@pytest.mark.parametrize(
    "cls, file",
    [
        (ClsWithInheritance, 'serializer/test/input/1.json'),
        (SimpleClass, 'serializer/test/input/2.json')
    ]
)
def test_class_pattern(cls, file):
    result = JsonSerializer().load(file)
    assert result(3, 7).__dict__ == cls(3, 7).__dict__
    assert result.__dict__.keys() == cls.__dict__.keys()


def test_class():
    serializer = JsonSerializer()
    serializer.dump(TestCls, 'serializer/test/output/3.json')
    res = serializer.load('serializer/test/output/3.json')
    assert TestCls().__dict__ == res().__dict__


def test_code():
    serializer = JsonSerializer()
    serializer.dump(clear_func.__code__, 'serializer/test/output/2.json')
    res = serializer.load('serializer/test/output/2.json')
    assert res == clear_func.__code__


@pytest.mark.parametrize(
    'filename',
    [
        'serializer/test/input/3.json',
        'serializer/test/input/4.json'
    ]
)
def test_invalid_json(filename):
    serializer = JsonSerializer()
    with pytest.raises(StopIteration):
        result = serializer.load(filename)


@pytest.mark.parametrize("test_input, expected",
                         [
                             (multiplier(3, 7).__closure__[0], '{ "cell_type": 7 }'),
                         ]
                         )
def test_cell(test_input, expected):
    serializer = JsonSerializer()
    assert serializer.dumps(test_input) == expected


def test_parse_digit_invalid():
    with pytest.raises(StopIteration):
        parse_digit("ffffffffff", 0)


@pytest.mark.parametrize('testdata, idx',
                         [
                             ("ffffffffff", 50),
                             ("****", 0)
                         ]
                         )
def test_parse_list_invalid(testdata, idx):
    with pytest.raises(StopIteration):
        parse_list(testdata, idx)


@pytest.mark.parametrize('testdata, idx',
                         [
                             ("ffffffffff", 50),
                             ("****", 0)
                         ]
                         )
def test_parse_dict_invalid(testdata, idx):
    with pytest.raises(StopIteration):
        parse_dict(testdata, idx)


def test_parse_symbol_invalid():
    with pytest.raises(StopIteration):
        parse_list("*", 0)


def test_parse_nan_nan():
    var, idx = parse_list("nan]", 0)
    assert idx == 4
