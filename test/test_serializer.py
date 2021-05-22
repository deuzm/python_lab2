import pytest

from serializer.json.json_serializer import JsonSerializer

z = 5


class SimpleClass:

    def __init__(self, x, y):
        self._x = x,
        self._y = y


def clear_func(x, y):
    return x + y


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
                '1.json'
        ),
        (
                TestClass,
                '2.json'
        ),
        (
                TestClass.class_m,
                '4.json'
        ),
        (
                clear_func,
                '5.json'
        ),
        (
            TestClass(3, 7),
            '6.json'
        )
    ]
)
def test(obj, expected):
    f = open('test/output/' + expected)
    result = f.read()
    result = result.replace('/', r'\\')
    assert JsonSerializer().dumps(
        obj
    ) == result

