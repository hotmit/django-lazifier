import re
from django.contrib.humanize.templatetags import humanize
from django.template import defaultfilters, Library
from django_lazifier.utils.builtin_types.obj import Obj
from django_lazifier.utils.builtin_types.str import Str


class Filter:
    filter_str = ''

    filter_name = ''
    filter_param = ''

    PARSE_REGEX = re.compile(r'(?P<filter>\w+?):[\'"](?P<param>.+?)[\'"]', re.IGNORECASE)

    def __init__(self, filter):
        self.filter_str = filter

        if not Str.contains(filter, ':'):
            self.filter_name = filter
        else:
            m = Filter.PARSE_REGEX.match(filter)
            if m:
                self.filter_name = m.group('filter')
                self.filter_param = m.group('param')
            else:
                raise ValueError('Invalid filter "%s"' % filter)

    def __str__(self):
        if self.filter_param:
            return "%s:'%s'" % (self.filter_name, self.filter_param)
        return self.filter_name

    def has_param(self):
        return len(self.filter_param) > 0

    def filter(self, obj, library: Library=None):
        filter_func = None
        if library:
            filter_func = Obj.getattr(library.filters, self.filter_name, None, execute_callable=False)

        if not filter_func or not callable(filter_func):
            filter_func = Obj.getattr(defaultfilters, self.filter_name, None, execute_callable=False)

        if not filter_func or not callable(filter_func):
            filter_func = Obj.getattr(humanize, self.filter_name, None, execute_callable=False)

        if not filter_func or not callable(filter_func):
            raise ValueError('Invalid filter "%s"' % self.filter_name)

        if self.has_param():
            return filter_func(obj, self.filter_param)
        return filter_func(obj)


class FilterParser:
    filter_list = None

    def __init__(self, filters_string: str):
        filters_string = filters_string.strip('|')

        self.filter_list = []
        filters = filters_string.split('|')
        for f in filters:
            self.filter_list.append(Filter(f))

    def pop_first(self) -> Filter:
        """
            Get the first filter in the list.

            :rtype : Filter
            :return:
            """
        return self.filter_list.pop(0)

    def __str__(self):
        if self.filter_list:
            return '|'.join([f.__str__() for f in self.filter_list])
        return ''
