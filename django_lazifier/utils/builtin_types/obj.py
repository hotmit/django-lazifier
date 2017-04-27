import sys
from collections import OrderedDict
from django.db import models
from django.db.models import Manager
from django.http import QueryDict
from django_lazifier.utils.builtin_types.iter import index_iter, last_iter
from django_lazifier.utils.builtin_types.str import Str
from django_lazifier.utils.builtin_types.dict import Dct


class Obj:

    @classmethod
    def get_dict(cls, obj, filter_list=None, exclude_list=None, verbose_key=False, get_display=False):
        """
        Extract a dict from the specified object.

        if None return OrderedDict()
        If model return {model_field_name: value, }
        If has __dict__ return __dict__
        If dict return self

        :type filter_list: list|None
        :type exclude_list: list|None
        :return: {dict}
        """
        if obj is None:
            return OrderedDict()

        if isinstance(obj, str) or isinstance(obj, int):
            return OrderedDict([(0, obj)])

        if isinstance(obj, QueryDict):
            return Dct.filter_and_exclude(obj.dict(), filter_list, exclude_list)

        if isinstance(obj, models.Model):
            result = OrderedDict()
            obj_dct = obj.__dict__

            for f in obj._meta.fields:
                field_value = obj_dct[f.attname] if f.attname in obj_dct else None
                if get_display:
                    get_display_func = 'get_%s_display' % f.attname
                    field_value = Obj.getattr(obj, get_display_func, field_value, execute_callable=True)
                result[f.attname] = field_value
            result = Dct.filter_and_exclude(result, filter_list, exclude_list)

            if verbose_key:
                try:
                    from django_lazifier.utils.django.model import Mdl
                except ImportError:
                    Mdl = sys.modules[__package__ + '.Mdl']

                verbose_result = OrderedDict()
                verbose_names = Mdl.get_field_verbose(obj._meta.model, list(result.keys()))
                for k, v in result.items():
                    if k in exclude_list:       # have to exclude here, because after this key becomes the verbose ver.
                        continue
                    name = verbose_names[k] if k in verbose_names else k
                    verbose_result[name] = v
                return verbose_result

            return result
        if isinstance(obj, tuple) or isinstance(obj, list):
            result = OrderedDict()
            for val, index in index_iter(obj):
                result[index] = val
            return Dct.filter_and_exclude(result, filter_list, exclude_list)

        if not isinstance(obj, dict):
            if Obj.has_func(obj, '__dict__'):
                return Dct.filter_and_exclude(obj.__dict__, filter_list, exclude_list)
            return OrderedDict()
        else:
            return Dct.filter_and_exclude(obj, filter_list, exclude_list)

    @classmethod
    def has_func(cls, obj, *args):
        """
        Check if obj has the specified function/method name(s).

        :param obj:
        :return:
        """
        methods = dir(obj)
        matched = [x for x in args if x in methods]
        return len(matched) == len(args)

    @classmethod
    def getattr(cls, obj, attr_name: str, default_value=None, execute_callable: bool = True):
        """
        Similar to native getattr() function,
        however it supports the dot notation to extract the sub-attr

        eg. Obj.getattr(person, "contact.name")
            This will first get the contact from the "person" object
            and then get the name from that.

        :param obj:
        :param attr_name: the attribute name, use dot to go further into sub-object eg. "doctor.phone_num".
        :param execute_callable: if attr is a function run the function and return the result
        :return:
        """
        if obj is None:
            return default_value

        not_found = 'getattr() Not Found'
        attr_name = str(attr_name)
        attrs = attr_name.split('.')

        # no name return none
        if not attrs:
            return default_value

        for att, last_item in last_iter(attrs):
            val = getattr(obj, att, not_found)

            # if not found using getattr then try to use some other alternative methods
            if val is not_found:
                # test positive int to get attr using index instead of name (ie. lists and tuples)
                if Str.is_positive_int(att) \
                        and (isinstance(obj, list) or isinstance(obj, tuple)):
                    index = int(att)
                    if index < len(obj):
                        val = obj[index]
                elif Obj.has_func(obj, '__getitem__', '__contains__'):
                    if att in obj:
                        val = obj[att]
                    elif Str.is_positive_int(att):
                        index = int(att)
                        if index in obj:
                            val = obj[index]

                if val is not_found:
                    return default_value

                if val is None and not last_item:
                    return default_value
            # endif not found

            if callable(val) and not isinstance(val, Manager) and execute_callable:
                # watch out for bound vs unbound method
                # ref: https://docs.python.org/3/library/inspect.html#inspect.ismethod
                # is bound method (ie. func of an instance, ie. not static)
                # if inspect.ismethod(val): (bounded, not use for now)
                val = val.__call__()

            obj = val

        return obj
