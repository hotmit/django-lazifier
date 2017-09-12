import base64
from decimal import Decimal
import re
from django.conf import settings
from django.template import defaultfilters
from django_lazifier.utils.utils import p


class Str:
    @classmethod
    def casefold(cls, the_str: str):
        """
        :type the_str: str
        :return:
        """
        if not the_str:
            return the_str

        return the_str.casefold()

    @classmethod
    def eq(cls, a: str, b: str, case=False):
        """
        Compare the to string see if they equal each other.
        :param a:
        :param b:
        :param case:
        :return:
        """
        if a is None and b is None:
            return True

        if a is None or b is None:
            return False

        if not case:
            return Str.casefold(a) == Str.casefold(b)

        return a == b

    @classmethod
    def contains(cls, haystack: str, *args, case=False):
        """
        Contains/contains_all - check to see if args is in they haystack
        :param haystack:
        :param args: the hay stack must contains all these
        :param case: case sensitive search
        :return:
        """
        try:
            from django_lazifier.utils.builtin_types.list import Lst
        except Exception as ex:
            print('Error: %s' % ex)

        if not case:
            haystack = Str.casefold(haystack)
            args = Lst.casefold(args)

        return Lst.all(args, lambda x: haystack.find(x) != -1)

    @classmethod
    def contains_any(cls, haystack: str, *args, case=False):
        """
        Check see if any of the args is inside of the haystack string.
        :param haystack:
        :param args:
        :param case:
        :return:
        """
        try:
            from django_lazifier.utils.builtin_types.list import Lst
        except Exception as ex:
            print('Error: %s' % ex)

        if not case:
            haystack = Str.casefold(haystack)
            args = Lst.casefold(args)

        return Lst.any(args, lambda x: haystack.find(x) != -1)

    @classmethod
    def int_val(cls, the_str, default_value=0):
        """
        Convert the string to int, if error occurred return default_value.
        :type the_str: str|byte
        :param the_str:
        :type default_value: int|None
        :param default_value:
        :return:
        """
        try:
            if the_str is None:
                return default_value

            if type(the_str) is str:
                the_str = the_str.strip()

            return int(round(float(the_str)))
        except ValueError:
            return default_value

    @classmethod
    def float_val(cls, the_str: str, default_value=0):
        """
        Convert string to float.

        :param the_str:
        :type default_value: int|float|None
        :param default_value:
        :return:
        """
        try:
            if type(the_str) is str:
                the_str = the_str.strip()

            return float(the_str)
        except ValueError:
            return default_value

    @classmethod
    def decimal_val(cls, the_str: str, default_value=0):
        """
        Convert string to decimal.

        :param the_str:
        :type default_value: int|Decimal|None
        :param default_value:
        :return:
        """
        try:
            if type(the_str) is str:
                the_str = the_str.strip()
                if len(the_str) == 0:
                    return default_value

            return Decimal(the_str)
        except Exception as ex:
            if settings.DEBUG:
                p('Exception: %s' % ex)
            return default_value

    @classmethod
    def base64_encode(cls, the_str: str, default_value=None):
        """
        Convert the string to utf-8 then encode with base64

        :param the_str:
        :type default_value: object|bool|None
        :return:
        """
        if not the_str:
            return ""

        try:
            return base64.encodebytes(the_str.encode('utf-8')).decode('utf-8').strip()
        except ValueError:
            return default_value

    @classmethod
    def base64_decode(cls, base64_str: str, default_value=None):
        """
        Decode the base64 string then return the utf-8 string.
        :param base64_str:
        :type default_value: object|bool|None
        :return:
        """
        if not base64_str:
            return ""

        try:
            return base64.decodebytes(base64_str.encode('utf-8')).decode('utf-8')
        except ValueError:
            return default_value

    @classmethod
    def break_camel(cls, the_str: str):
        """
        Turn a camel case string to title case.
        eg. helloWorld => Hello World
        :param the_str: str
        :return: str
        """
        if the_str is None:
            return ''
        return re.sub("([a-z])([A-Z])", "\g<1> \g<2>", the_str).title()

    @classmethod
    def snake_to_camel(cls, the_str):
        """
        Convert snake case into camel case. e.g. convert python var to js var, the_string into theString.
        :param the_str: the snake case string
        :return:
        """
        return re.sub(r'_([a-z])', lambda m: m.group(1).upper(), the_str)

    @classmethod
    def snake_to_title(cls, the_str):
        """
        Convert snake case string to title
        :param the_str:
        :return:
        """
        if not the_str:
            return the_str

        the_str = the_str.replace('_', ' ')
        the_str = re.sub(r'\s+', ' ', the_str)
        return the_str.title()

    @classmethod
    def snake_to_kebab(cls, the_str):
        """
        Convert snake_case to kebab-case.

        :param the_str: the snake case string
        :return: kebab-case.
        """
        return the_str.replace('_', '-').lower()

    @classmethod
    def is_int(cls, the_str: str):
        if the_str is None:
            return False

        the_str = str(the_str)

        if len(the_str) == 0 or the_str == '-0':
            return False

        if the_str.startswith('-'):
            the_str = the_str[1:]

        return the_str.isdigit()

    @classmethod
    def is_positive_int(cls, the_str: str):
        """
        Determine if the string is a positive integer.

        :param the_str:
        :return: bool
        """
        if the_str is None:
            return False
        return the_str.isdigit()

    @classmethod
    def to_css_id(cls, the_str: str):
        if not the_str:
            return ''

        the_str = Str.break_camel(the_str)
        the_str = the_str.replace('_', ' ').strip()

        regex = re.compile(r'^\d+')
        the_str = regex.sub('', the_str)

        regex = re.compile(r'\W+')
        the_str = regex.sub(' ', the_str)

        regex = re.compile(r'\s+')
        the_str = regex.sub(' ', the_str)

        return the_str.replace(' ', '-').lower().strip('-')

    @classmethod
    def format_traceback(cls, the_str: str):
        the_str = defaultfilters.escape(the_str)

        the_str = re.sub('\n', '<br />\n', the_str)
        the_str = re.sub('\s', '&nbsp;', the_str)

        the_str = defaultfilters.mark_safe(the_str)

        return the_str

    @classmethod
    def format_display_int(cls, number: int, comma_separated=True, default_value='-'):
        try:
            if number is None:
                return default_value

            number = int(number)
            if comma_separated:
                result = '{0:,d}'.format(number)
            else:
                result = '{0:d}'.format(number)
            return result
        except Exception as ex:
            if settings.DEBUG:
                p('Exception: %s' % ex)
            return default_value

    @classmethod
    def split_parts(cls, the_str: str, sep: str, max_split, default_values: list, left_to_right=True):
        """
        Split string into multiple parts.
            eg. width, height = Str.split_parts('100x300', 'x', 1, [200, 200])

        :param the_str:
        :param sep:
        :param max_split:
        :param default_values:
        :param left_to_right:
        :return:
        """
        if not the_str:
            return default_values

        params = [sep, max_split]
        if left_to_right:
            result = the_str.split(*params)
        else:
            result = the_str.rsplit(*params)

        if result and len(result) == max_split + 1:
            return result

        return default_values

    @classmethod
    def format_display_float(cls, number, comma_separated=True,
                             decimal_places=2, trim_zeros=True, default_value='-'):
        """
        Format number for display.

        :param default_value:
        :param trim_zeros:
        :param decimal_places:
        :param comma_separated:
        :type number: {float|Decimal}
        """
        try:
            if number is None:
                return default_value

            number = float(number)
            decimal_places = int(decimal_places)
            format_str = '{0:'
            if comma_separated:
                format_str += ','
            if decimal_places > 0:
                format_str += '.' + decimal_places.__str__()
            format_str += 'f}'
            result = format_str.format(number)
            if trim_zeros:
                result = result.rstrip('0').rstrip('.')
            return result
        except Exception as ex:
            if settings.DEBUG:
                p('Exception: %s' % ex)
            return default_value

    @classmethod
    def title_to_snake(cls, the_str: str):
        """
        Convert title case to snake case ('Hello World' => 'hello_world')
        :param the_str:
        :return:
        """
        if not the_str:
            return the_str
        the_str = cls.break_camel(the_str)
        return the_str.lower().replace(' ', '_')
