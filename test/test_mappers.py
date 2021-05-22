import pytest
import collections
from serializer.json.mappers import *


def compare(x, y):
    return collections.Counter(x) == collections.Counter(y)


def clear_func(x, y):
    return x + y

z = 5

class SimpleClass:

    def __init__(self, x, y):
        self._x = x,
        self._y = y

class TestClass(SimpleClass):


    def __init__(self, x, y):
        super().__init__(x, y)
        self._x = x,
        self._y = y

    @staticmethod
    def static_m():
        global z
        clear_func(1, 2)

    def class_m_2(self):
        self.class_m()

    def class_m(self):
        print(5 + 7)

def multiplier(n, d):
    """Return a function that multiplies its argument by n/d."""
    def multiply(x):
        """Multiply x by n/d."""
        return x * n / d
    return multiply


def side_func(x, y):
    global z
    z = x + y
    t = TestClass()
    return clear_func(x, y)


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

