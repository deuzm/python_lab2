import collections


def compare(x, y):
    return collections.Counter(x) == collections.Counter(y)


def clear_func(x, y):
    return x + y


z = 5


class Empty_cls:
    pass


class ClsWithInheritance(Empty_cls):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class TestCls:

    @staticmethod
    def static_m():
        global z
        clear_func(1, 2)

    def class_m_2(self):
        self.class_m()

    def class_m(self):
        print(5 + 7)


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
