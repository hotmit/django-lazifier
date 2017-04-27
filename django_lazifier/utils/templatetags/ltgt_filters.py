import time
import collections
from os import path
from django import template
from django.db.models import Manager
from django.template.loader import render_to_string
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from collections import OrderedDict
from django_lazifier.ltgt.templatetags.helper.filter_parser import FilterParser
from django_lazifier.utils.builtin_types.list import Lst
from django_lazifier.utils.builtin_types.obj import Obj
from django_lazifier.utils.builtin_types.str import Str
from django_lazifier.utils.django.model import Mdl
from django_lazifier.utils.json.json import Json

register = template.Library()


@register.filter
def index(obj, attr_name):
    """
    Return the index of the list/dict

    :param obj:
    :param attr_name: supports dot notation (eg. person|index:"contact.phone" where contact is attribute of person)
    :return:
    """
    return get_attr(obj, attr_name)


@register.filter
def get_attr(obj, attr_name):
    """
    Return the index of the list/dict

    :param obj:
    :param attr_name: supports the dot notation
        (eg. person|index:"contact.phone" where contact is attribute of person)
    :return:
    """
    try:
        result = Obj.getattr(obj, attr_name, None)
        return result
    except:
        return None


@register.filter
def get_display(obj, attr_name):
    try:
        display_name = 'get_%s_display' % attr_name
        result = Obj.getattr(obj, display_name, None)

        if result is None:
            result = Obj.getattr(obj, attr_name, None)

        return result
    except:
        return None


@register.filter
def apply_filter(obj, filter_list):
    """
    Run a list of filter based on the specified string.

    my_format_var = "|date:'Y/m/d'"
    eg. my_date|apply_filter:my_format_var

    :param obj:
    :param filter_list:
    :return:
    """
    if obj is None or filter_list is None or len(filter_list) == 0:
        return obj

    filters = FilterParser(filter_list)

    if filters.filter_list:
        f = filters.pop_first()
        new_obj = f.filter(obj, register)

        if filters.filter_list:
            return apply_filter(new_obj, filters.__str__())
        else:
            return new_obj

    return obj


@register.filter
def negate(obj):
    """
    Toggle boolean value or reverse the sign of an integer.

    :param obj:
    :return:
    """
    try:
        if isinstance(obj, bool):
            return not obj

        return -1 * int(obj)
    except:
        return obj


@register.filter(is_safe=True)
def jsonify(obj):
    """
    Convert the specified obj into json string.

    :param obj:
    :return:
    """
    return mark_safe(Json.to_json(obj))


@register.filter(is_safe=True)
def base64_encode(obj):
    """
    Base64 encode the specified string.
    :param obj:
    :return:
    """
    return mark_safe(Str.base64_encode(obj))


@register.filter(is_safe=True)
def base64_decode(obj):
    """
    Decode using base64
    :param obj:
    :return:
    """
    return mark_safe(Str.base64_decode(obj))


@register.filter(is_safe=True)
def trans(the_str):
    """
    Translate the specified string.
    :param the_str:
    :return:
    """
    return mark_safe(_(the_str))


@register.filter(is_safe=True)
def basename(file_path):
    """
    Return the name of the file.
    :param file_path:
    :return:
    """
    return mark_safe(path.basename(file_path))


@register.filter(is_safe=True)
def display_error(errors):
    if not errors:
        return mark_safe('')

    if isinstance(errors, list):
        if len(errors) == 1:
            errors = errors.pop()
        else:
            ul = '<ul class="error-list">'
            for err in errors:
                ul += '<li>{error}</li>'.format(error=err)
            ul += '</ul>'
            errors = ul

    return mark_safe('<div class="alert alert-danger" role="alert">{errors}</div>'.format(errors=errors))


@register.filter
def epoch(value):
    """
    Convert datetime to unix epoch time.
    Alternatively you can you this {{ my_date|date:"U" }}

    :param value: datetime instance
    :return: int
    """
    try:
        return int(time.mktime(value.timetuple()) * 1000)
    except AttributeError:
        return ''


@register.filter
def join_by(the_list, options):
    """
    Join the list.
        Usage:  facilities|join_by:" ,zone.name"   => facility1 facility2
                facilities|join_by:", ,zone.name"   => facility1, facility2

    :param the_list:
    :param options: comma separated "{separator}, {attribute.inner_attribute}".
    :return: string
    """
    if not the_list:
        return ''
    assert options, 'join_by: Arguments cannot be emptied.'

    if isinstance(the_list, Manager):
        the_list = the_list.all()
    elif callable(the_list):
        the_list = the_list.__call__()

    separator, attr = options.rsplit(',', 1)
    attr = attr.strip()
    return separator.join([Obj.getattr(itm, attr, '').__str__() for itm in the_list])


@register.filter
def join_str(the_list, none_value='-'):
    """
    :return: string
    """
    if not the_list:
        return ''

    result = []
    for item in the_list:
        if not item:
            result.append(none_value)
        elif type(item) is str:
            result.append(item)
        else:
            result.append(item.__str__())
    return ', '.join(result)


@register.filter
def trans_join(the_list, separator):
    """
    Translate and join the list.
        Usage: list|trans_join_by:", "

    :param the_list:
    :param separator:
    :return:
    """
    if not the_list:
        return ''
    return separator.join([_(x) for x in the_list])


@register.filter
def build_list(the_list, attr_name):
    """
    Extract attr from each item in the list

    :param the_list:
    :param attr_name: attribute name support .dot notation (eg. list_of_people|build_list:"contact.phone"
    :return: list
    """
    return [Obj.getattr(x, attr_name, None) for x in the_list]


@register.filter
def filter_attr(the_dict, attr_names):
    """
    Only return the item that in the attr_names list

    :param the_dict:
    :param attr_names: comma separated names
    :return: dict
    """

    if isinstance(the_dict, dict):
        attrs = attr_names.split(',')
        return dict((k, v) for k, v in the_dict.items() if k.strip() in attrs)

    return the_dict


@register.filter
def display(choices, value):
    """
    Get the display value for the selected choice. ie. get_FIELD_display()
    :type choices: dict|tuple
    :param choices: FIELD_CHOICE
    :param value: the value of the tuple
    :return: string
    """
    if not choices:
        return value

    if isinstance(choices, tuple):
        choices = OrderedDict(choices)

    return choices.get(value, value)


@register.filter
def as_table(data, filter_param=None):
    """
    Turn queryset or list row_dict into a table.
    :param data: queryset|list of [row_dict]
    :param filter_param: comma separated list of column. Syntax: queryset|as_table:'include_me, !not_include, include2'
                            eg. users|as_table:'!age, !password'
                            eg. group|as_table:'name, group_count'
    :return:
    """
    if not data:
        return None

    result = []
    filter_list = []
    exclude_list = []
    model = Obj.getattr(data, 'model', None, False)

    if filter_param:
        filter_param_list = Lst.strip_string(filter_param.split(','))
        for the_filter in filter_param_list:
            assert isinstance(the_filter, str)
            if the_filter.startswith('!'):
                exclude_list.append(the_filter[1:])
            else:
                filter_list.append(the_filter)

    if isinstance(data, dict):
        sub_tables = {}
        for key, row in data.items():
            if isinstance(row, list):
                sub_tables[key] = as_table(row, filter_param)
                continue

            row_dict = Obj.get_dict(row, filter_list, exclude_list, verbose_key=True, get_display=True)
            result.append(row_dict)

        if sub_tables:
            context = {'sub_tables': sub_tables}
            html = render_to_string('ltgt/table_filter/as_table_filter_sub_tables_layout.html', context)
            return mark_safe(html)
    else:
        if isinstance(data, collections.Iterable):
            for row in data:
                row_dict = Obj.get_dict(row, filter_list, exclude_list, verbose_key=True, get_display=True)

                for k, v in row_dict.items():
                    if isinstance(v, list):
                        if v:
                            row_dict[k] = as_table(v, filter_param)

                result.append(row_dict)
        else:
            result.append(Obj.get_dict(data, verbose_key=True))

    if result:
        headers = []
        if model is not None:
            columns = result[0].keys()
            headers = list(Mdl.get_field_verbose(model, columns).values())
        else:
            for k, v in result[0].items():
                if Str.is_int(k):
                    headers.append(type(v).__name__)
                elif type(k) is str and k.islower():
                    headers.append(Str.snake_to_title(k))
                else:
                    headers.append(k)

        context = {'headers': headers, 'data': result}
        html = render_to_string('ltgt/table_filter/as_table_filter_layout.html', context)
    else:
        return None

    return mark_safe(html)


@register.filter
def as_css_id(the_str, post_fix=None):
    """
    Format the specified string as valid css_id value. "123 Hello $2" => "hello-2"
    :param the_str:
    :param post_fix:
    :return:
    """
    css_id = Str.to_css_id(the_str)
    if post_fix is not None:
        css_id += post_fix.__str__()
    return css_id


@register.filter
def as_checkbox(bool_value, classes=None):
    """
    Display bool as check mark

    :param bool_value:
    :param classes: comma separated css classes. Checked class follow by unchecked. eg. fa-check-square-o, fa-square-o
    :return:
    """
    if bool_value is None:
        return mark_safe('-')

    checked = 'glyphicon glyphicon-ok'
    unchecked = 'glyphicon glyphicon-remove'

    if classes:
        assert isinstance(classes, str)
        parts = classes.split(',')
        if len(parts) == 2:
            checked = parts[0]
            unchecked = parts[1]

    icon_class = checked if bool_value else unchecked
    icon_class = icon_class.strip()

    result = '<i class="{css_class}"></i>'.format(css_class=icon_class)
    return mark_safe(result)


@register.filter
def as_link(link, icon_class=None):
    """
    Display link as an icon.

    :param link:
    :param icon_class:
    :return:
    """
    if not link:
        return mark_safe('-')

    if not icon_class:
        icon_class = 'fa fa-file-o'

    if hasattr(link, 'url'):
        link = link.url

    title = basename(link)
    title = escape(title)

    result = '<a href="{href}" target="_blank" title="{title}"><i class="{icon_class}"></i></a>' \
        .format(href=link, title=escape(title), icon_class=icon_class)
    return mark_safe(result)


@register.filter
def as_text_link(link, link_text=None):
    """
    Display link as a link.

    :param link:
    :return:
    """
    if not link:
        return mark_safe('-')

    if hasattr(link, 'url'):
        link = link.url

    title = basename(link)
    title = escape(title)

    link_text = link_text or title

    result = '<a href="{href}" title="{title}">{link_text}</a>' \
        .format(href=link, title=escape(title), link_text=link_text)
    return mark_safe(result)


@register.filter
def as_image_link(link, icon_class=None):
    """
    Display image as a link icon.

    :param link:
    :param icon_class:
    :return:
    """
    if not link:
        return mark_safe('-')

    if not icon_class:
        icon_class = 'fa fa-file-image-o'

    if hasattr(link, 'url'):
        link = link.url

    title = basename(link)
    title = escape(title)

    result = '<a class="image-link" rel="image-attachment" href="{href}" target="_blank" title="{title}">' \
             '<i class="{icon_class}"></i></a>' \
        .format(href=link, title=escape(title), icon_class=icon_class)
    return mark_safe(result)


@register.filter
def as_tooltip(text, icon_class=None):
    """
    Display text as a tooltip icon

    :param text:
    :param icon_class:
    :return:
    """
    if not text:
        return mark_safe('-')

    if not icon_class:
        icon_class = 'fa fa-commenting-o'

    result = '<i class="{icon_class}" data-toggle="tooltip" title="{title}"></i>' \
        .format(title=escape(text), icon_class=icon_class)
    return mark_safe(result)


@register.filter
def as_image(link, classes=''):
    if not link:
        return None

    if hasattr(link, 'url'):
        link = link.url

    if classes:
        classes = ' %s' % classes.strip()

    title = basename(link) or link
    result = '<img class="ltgt-img{classes}" src="{link}" title="{title}" />' \
        .format(link=escape(link), title=escape(title), classes=escape(classes))
    return mark_safe(result)


@register.filter
def as_thumbnail(link, dimension='200x300'):
    if not link:
        return None

    if hasattr(link, 'url'):
        link = link.url

    width, height = Str.split_parts(dimension, 'x', 1, [200, 300])

    title = basename(link) or link
    result = '<a class="ltgt-img-link" href="{link}" title="{title}"><img class="ltgt-thumbnail" src="{link}" alt="" ' \
             'style="max-width: {width}px; max-height={height}px" /></a>' \
        .format(link=escape(link), title=escape(title), width=width, height=height)
    return mark_safe(result)


@register.filter
def is_type(obj, type_name):
    """
    Type check based on class name.

    :param obj:
    :param type_name:
    :return:
    """
    is_same_type = type(obj).__name__ == type_name
    return is_same_type


@register.filter
def pop(obj, key_name=None):
    """
    Remove the indexed item from the collection and return the removed value. Similar to dict.pop(key_name).
    :param obj:
    :param key_name: key name or index
    :return:
    """
    if key_name is None:
        if isinstance(obj, list):
            return obj.pop()
        k, v = obj.popitem()
        return v
    return obj.pop(key_name)


@register.filter
def create_range(end_index, start_index=0):
    """
    range(start_index, end_index)

    :param end_index: non inclusive start_index=10 => 0 .. 9 (10 items)
    :param start_index: default is 0
    :return: [start .. end]
    """
    return range(start_index, int(end_index))


@register.filter
def record_counts(records, default_value='0'):
    if not records:
        return default_value

    try:
        return len(records)
    except Exception as ex:
        return default_value
