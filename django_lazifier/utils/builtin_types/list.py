from collections import OrderedDict
import random
from django_lazifier.utils.builtin_types.obj import Obj
from django_lazifier.utils.builtin_types.str import Str
from django_lazifier.utils.utils import log_exception


class Lst:
    @classmethod
    def get_random(cls, the_list: list, pop=False, default_value=None):
        """
        Get one item at random in the specified list.

        :param the_list:
        :param pop:
        :param default_value:
        :return:
        """
        if not the_list:
            return default_value

        length = len(the_list)
        rand_index = random.randint(0, length-1)

        if pop:
            return the_list.pop(rand_index)

        return the_list[rand_index]

    @classmethod
    def casefold(cls, str_list):
        """
        Pass each string element through str.casefold()
        :param str_list:
        :return:
        """
        return [str(x).casefold() for x in str_list]

    @classmethod
    def convert_to_int(cls, str_list):
        """
        Convert a list of string into a list of int
        :param str_list: ["1", "2.99", "0.11"] => [1, 3, 0]
        :return: []
        """
        if not str_list:
            return []

        int_list = []
        for s in str_list:
            val = Str.int_val(s, None)
            if val is not None:
                int_list.append(val)

        return int_list

    @classmethod
    def convert_to_str(cls, the_list):
        """
        Convert a list of object into a list of string
        :return: []
        """
        if not the_list:
            return []

        result = []
        for s in the_list:
            if s is not None:
                result.append(s.__str__())

        return result

    @classmethod
    def strip_string(cls, the_list, chars=None):
        """
        Trim the list of strings.
        :param the_list:
        :param chars:
        :return:
        """
        the_list = Lst.convert_to_str(the_list)
        return [elm.strip(chars) for elm in the_list]

    @classmethod
    def group_by(cls, the_list, group, none_value_label='None', flat=False):
        """
        Put all
        :param the_list:
        :param group: {str} name of the attribute, support dot notation group_by(persons, 'contact.phone')
        :param none_value_label: the value of the column specified is None then use this label as the key.
        :return:
        """
        result = OrderedDict()
        for row in the_list:
            col_value = Obj.getattr(row, group, None)
            if col_value is None:
                col_value = none_value_label

            if not flat and col_value not in result:
                result[col_value] = []

            if flat:
                result[col_value] = row
            else:
                result[col_value].append(row)
        return result

    @classmethod
    def multi_group_by(cls, the_list, none_value_label, group_names: list):
        """
        Provide a drilled down version of the data.
        eg. Lst.multi_group_by(sensors, _('Unassigned'), ['facility__id', 'zone__id'])

        return { facility_1 : [ {zone_1 : [ {sensor_1},
                                            {sensor_2} ],
                                {zone_2 : [ {sensor_3},
                                            {sensor_4} ]

        :type the_list: list|QuerySet|ValuesQuerySet
        :param the_list: list, QuerySet or ValuesQuerySet
        :type none_value_label: str|None|object
        :param none_value_label: the value to use if the column value is None
        :param group_names: the list of columns to group by
        :return: List
        """
        if type(group_names) == str:
            group_names = [group_names]

        if not isinstance(group_names, list):
            raise ValueError('The argument group_names must be a list of all the columns you want to group.')

        group_names = group_names.copy()
        if group_names:
            col = group_names.pop(0)
            result = Lst.group_by(the_list, col, none_value_label)
            if group_names:
                for col, rows in result.items():
                    result[col] = Lst.multi_group_by(rows, none_value_label, group_names)

            return result
        return OrderedDict()

    @classmethod
    def tuple_multi_group_by(cls, the_list, none_value_label, group_names: list):
        """
        Similarly to multi_group_by but instead of use the value of the specified columns
        as a key it combine all the keys together in one tuple as key.

        eg. sensors = Sensor.objects.values(**columns)
            Lst.tuple_multi_group_by(sensors, 'None', ['facility__id', 'zone__id'])

        return { (facility_1, zone_1): [ sensor1, sensor2 ],
                 (facility_1, zone_2): [ sensor3 ],
                 (facility_2, zone_3): [ sensor4 ])

        :type the_list: list|QuerySet|ValuesQuerySet
        :param the_list: list, QuerySet or ValuesQuerySet
        :param none_value_label: the value to use if the column value is None
        :param group_names: the list of columns to group by
        :return: List
        """
        if type(group_names) == str:
            group_names = [group_names]

        if not isinstance(group_names, list):
            raise ValueError('The argument group_names must be a list of all the fields you want to group.')

        group_names = group_names.copy()
        if group_names:
            result = OrderedDict()
            first_grp_val = group_names.pop(0)  # pop at the start
            first_group_by = Lst.group_by(the_list, first_grp_val, none_value_label)

            if group_names:
                for col, rows in first_group_by.items():
                    tuple_list = Lst.tuple_multi_group_by(rows, none_value_label, group_names)
                    for k, t in tuple_list.items():
                        result[(col,) + k] = t
            else:
                for k, v in first_group_by.items():
                    result[(k,)] = v
            return result

        return OrderedDict()

    @classmethod
    def all(cls, the_list, func, **kwargs):
        """
        Return True if all is True, else False.
            Similar to all() but its accept a lambda.

        :param the_list:
        :param func: lambda that return bool
        :param kwargs: any additional params for func
        :return:
        """
        for i in the_list:
            if not func(i, **kwargs):
                return False

        return True

    @classmethod
    def any(cls, the_list, func, **kwargs):
        """
        Return True if any is True, else False.
            Similar to any() but its accept a lambda.

        :param the_list:
        :param func: lambda that return bool
        :param kwargs: any additional params for func
        :return:
        """
        for i in the_list:
            if func(i, **kwargs):
                return True

        return False

    @classmethod
    def prep_select_optgroups(cls, the_list, opt_groups: list, value_attr, display_attr, none_value_label):
        """
        Prep list to be use as a choice for the ChoiceField

            eg. sensor_choices = Lst.prep_select_optgroups(sensors, ['facility.name', 'zone.name'],
                                               'id', 'sensor_name', _('Unassigned Sensors'))

        :param the_list: ValueQuerySet, QuerySet or list
        :param opt_groups: the group column/attr name or index
        :param value_attr: the option value
        :param display_attr: the option display text
        :return:
        """
        groups = Lst.tuple_multi_group_by(the_list, none_value_label, opt_groups)

        if groups:
            result = []
            for tp, arr in groups.items():
                og_header = ' > '.join(tp)
                og_list = []
                for row in arr:
                    og_list.append((Obj.getattr(row, value_attr), Obj.getattr(row, display_attr),))
                result.append((og_header, tuple(og_list),))
            return tuple(result)

        return groups

    @classmethod
    def get_unique(cls, the_list, default_value=None, unique_attr=None):
        """
        Get a list of unique values in the list, default_value is [] if default_value is set to None.

        :param the_list:
        :param default_value: if none value is []
        :param unique_attr: select your own unique attribute (in case when the object is unhashable
                                or you want your own attr)
        :rtype list
        """
        if default_value is None:
            default_value = []

        if not the_list:
            return default_value

        try:
            # Src: http://stackoverflow.com/questions/480214
            #       /how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
            # Src: http://www.peterbe.com/plog/uniqifiers-benchmark
            if unique_attr is None:
                added_list = set()
                add_to_added_list = added_list.add  # this static ref for performance reason
                return [x for x in the_list if not (x in added_list or add_to_added_list(x))]

            result = []
            existed_item = {}               # dict is much faster than list when checking existence of a key
            for itm in the_list:
                key = Obj.getattr(itm, unique_attr)
                if key not in existed_item:
                    result.append(itm)
                    existed_item[key] = None
            return result
        except Exception as ex:
            log_exception(ex)
            return default_value

    @classmethod
    def reverse(cls, the_list: list):
        """
        Reverse the order of the items in the list.
        :param the_list:
        :return:
        """
        if not list:
            return []
        # return list(reversed(the_list))
        return the_list[::-1]

    @classmethod
    def contains_all(cls, the_list, *args):
        """
        Check to see if the_list contains all of the args

        :param the_list: the haystack
        :param args: the needle
        :return:
        """
        return Lst.all(args, lambda x: x in the_list)

    @classmethod
    def contains_any(cls, the_list, *args):
        """
        Check to see if the_list contains any of the args

        :param the_list: the haystack
        :param args: the needle
        :return:
        """
        return Lst.any(args, lambda x: x in the_list)

    @classmethod
    def unordered_list_equals(cls, lst_a, lst_b):
        if not isinstance(lst_a, list) or not isinstance(lst_b, list):
            return False

        if lst_a == lst_b:
            return True

        if len(lst_a) != len(lst_b):
            return False

        return set(lst_a) == set(lst_b)

    @classmethod
    def str_join(cls, lst, separator=', ', value_attr: str=None):
        if not lst:
            return ''

        str_list = []
        for itm in lst:
            if value_attr is not None:
                itm = Obj.getattr(itm, value_attr)
            itm = str(itm)
            str_list.append(itm)
        return separator.join(str_list)
