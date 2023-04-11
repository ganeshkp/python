# https://python-course.eu/advanced-python/iterable-iterator.php

cities = ["Berlin", "Vienna", "Zurich"]
iterator_obj = iter(cities)
print(iterator_obj)
print(next(iterator_obj))
print(next(iterator_obj))
print(next(iterator_obj))
# print(next(iterator_obj))

# ------------------------------------------------


def iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


# for element in [34, [4, 5], (4, 5), {"a": 4}, "dfsdf", 4.5]:
#     print(element, "iterable: ", iterable(element))

# ---------------------------------------------------------------


class Reverse:
    """
    Creates Iterators for looping over a sequence backwards.
    """

    def __init__(self, data):
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]


# lst = [34, 978, 42]
# lst_backwards = Reverse(lst)
# for el in lst_backwards:
#     print(el)

# -------------------------------------------


class Counter:
    def __init__(self, low, high):
        self.current = low - 1
        self.high = high

    def __iter__(self):
        return self

    def __next__(self):  # Python 2: def next(self)
        self.current += 1
        if self.current < self.high:
            return self.current
        raise StopIteration


for c in Counter(3, 9):
    print(c)
