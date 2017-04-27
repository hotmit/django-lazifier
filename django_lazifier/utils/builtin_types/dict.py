import sys
from collections import OrderedDict


class Dct:
    @classmethod
    def filter(cls, the_dict: dict, key_list: list):
        """
        Return only items that the keys are in key_list

        :param the_dict:
        :param key_list:
        :return:
        """
        if not the_dict:
            return OrderedDict()

        if not key_list:
            return the_dict

        return OrderedDict([(key, the_dict[key]) for key in key_list if key in the_dict])

    @classmethod
    def exclude(cls, the_dict: dict, key_list: list):
        """
        Remove specified keys from dict
        :param the_dict:
        :param key_list:
        :return:
        """
        if not the_dict:
            return OrderedDict()

        if not key_list:
            return the_dict

        return OrderedDict([(key, value) for key, value in the_dict.items() if key not in key_list])

    @classmethod
    def filter_and_exclude(cls, the_dict: dict, filter_list: list = None, exclude_list: list = None):
        """
        Filter then follow by exclude.

        :type exclude_list: list of [str]
        :type filter_list: list of [str]
        :param the_dict:
        :param filter_list: only keep the keys in this collection.
        :param exclude_list: remove any key not in this list
        :return:
        """
        the_dict = Dct.filter(the_dict, filter_list)
        the_dict = Dct.exclude(the_dict, exclude_list)
        return the_dict

    @classmethod
    def to_string(cls, the_dict: dict, excludes=None):
        """
        Convert dict to comma separated string.
            eg. name="John Doe", age="27"
        :param the_dict:
        :return: str
        """
        if not the_dict:
            return ''

        if 0 in the_dict.keys():
            val = the_dict[0]
            if isinstance(val, str) or isinstance(val, int):
                return '"%s"' % val

        lst = Dct.exclude(the_dict, excludes).items()
        result = []
        for k, v in lst:
            if isinstance(v, dict):
                dct_txt = Dct.to_string(v, excludes=excludes)
                result.append('%s={ %s }' % (k, dct_txt))
            elif isinstance(v, list):
                list_items = []
                for i in v:
                    if isinstance(i, dict):
                        list_items.append('{ %s }' % Dct.to_string(i, excludes=excludes))
                    elif i is not None:
                        list_items.append('"%s"' % i.__str__())
                    else:
                        list_items.append('None')

                lst_txt = '[ %s ]' % ', '.join(list_items)
                result.append('%s=%s' % (k, lst_txt))
            else:
                result.append('%s="%s"' % (k, v))
        return ', '.join(result)

    @classmethod
    def diff(cls, old_dict: dict, new_dict: dict, excludes=None):
        """
        Compare two diff

        :param old_dict:
        :param new_dict:
        :param excludes:
        :return:
        """
        try:
            from django_lazifier.utils.builtin_types.obj import Obj
        except ImportError:
            Obj = sys.modules[__package__ + '.Obj']

        if not isinstance(old_dict, dict):
            old_dict = Obj.get_dict(old_dict) or OrderedDict()

        if not isinstance(new_dict, dict):
            new_dict = Obj.get_dict(new_dict) or OrderedDict()

        result = OrderedDict()

        if not old_dict:
            for k, v in new_dict.items():
                if excludes is None or k not in excludes:
                    result[k + '_new'] = v
            return result

        for k, v in old_dict.items():
            if excludes is None or k not in excludes:

                if isinstance(v, dict):
                    result[k] = Dct.diff(v, new_dict.get(k, {}), excludes=excludes)
                    continue

                if k not in new_dict:
                    result[k + '_removed'] = v
                elif v != new_dict[k]:
                    result[k + '_old'] = v
                    result[k + '_new'] = new_dict[k]

        for k, v in new_dict.items():
            if excludes is None or k not in excludes:
                if k not in old_dict:
                    result[k + '_added'] = v

        return result


# region [ DefaultOrderedDict ]
from collections import OrderedDict, Callable

class DefaultOrderedDict(OrderedDict):
    # Source: http://stackoverflow.com/a/6190500/562769
    def __init__(self, default_factory=None, *a, **kw):
        if (default_factory is not None and
           not isinstance(default_factory, Callable)):
            raise TypeError('first argument must be callable')
        OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, self.items()

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        import copy
        return type(self)(self.default_factory,
                          copy.deepcopy(self.items()))

    def __repr__(self):
        return 'OrderedDefaultDict(%s, %s)' % (self.default_factory,
                                               OrderedDict.__repr__(self))
# endregion
