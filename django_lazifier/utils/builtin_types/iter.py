

def last_iter(iterable):
    """
    for x, is_last_iter in last_iter(range(3)):
        print x, is_last_iter

    0, False    1, False    2, True

    :param iterable:
    :return:
    """
    it = iter(iterable)
    last = next(it)  # it.next() in Python 2
    for val in it:
        yield last, False
        last = val
    yield last, True


def index_iter(iterable):
    """
    for x, index0 in index_iter(range(3)):
        print x, index0

    :param iterable:
    :return:
    """
    index = 0
    for val in iterable:
        yield val, index
        index += 1


class IterBase:
    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        return True
