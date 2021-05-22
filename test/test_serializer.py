import pytest

from json_serializer.json_serializer import JsonSerializer
from test.utils import *


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
                'test/output/1.json'
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
        (ClsWithInheritance, 'test/input/1.json'),
        (SimpleClass, 'test/input/2.json')
    ]
)
def test_class_pattern(cls, file):
    result = JsonSerializer().load(file)
    assert result(3, 7).__dict__ == cls(3, 7).__dict__
    assert result.__dict__.keys() == cls.__dict__.keys()


def test_class():
    serializer = JsonSerializer()
    serializer.dump(TestCls, 'test/output/3.json')
    res = serializer.load('test/output/3.json')
    assert TestCls().__dict__ == res().__dict__


def test_code():
    serializer = JsonSerializer()
    serializer.dump(clear_func.__code__, 'test/output/2.json')
    res = serializer.load('test/output/2.json')
    assert res == clear_func.__code__

def test_invalid_json():
    serializer = JsonSerializer()
    with pytest.raises(StopIteration):
        result = serializer.load('test/input/3.json')

@pytest.mark.parametrize("test_input, expected",
                         [
                             (multiplier(3, 7).__closure__[0], '{ "cell_type": 7 }'),
                         ]
                         )
def test_cell(test_input, expected):
    serializer = JsonSerializer()
    assert serializer.dumps(test_input) == expected

