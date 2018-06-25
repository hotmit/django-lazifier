from collections import OrderedDict
import inspect
import re
from types import BuiltinFunctionType
from django import template
from django.utils.safestring import mark_safe
from markupsafe import escape
from django_lazifier.utils.builtin_types.obj import Obj

register = template.Library()


class AssignNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def render(self, context):
        context[self.name] = self.value.resolve(context, True)
        return ''


@register.tag
def assign(parser, token):
    """
    Assign an expression to a variable in the current context.
    
    Syntax::
        {% assign [name] [value] %}
    Example::
        {% assign list entry.get_related %}
        
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])
    return AssignNode(bits[1], value)


class RangeNode(template.Node):
    def __init__(self, num, context_name):
        self.num = template.Variable(num)
        self.context_name = context_name

    def render(self, context):
        context[self.context_name] = range(int(self.num.resolve(context)))
        return ""


@register.tag
def tag_range(parser, token):
    """
    {% range 100 as my_range %}
    {% for i in my_range %}
      {{ i }}: Something I want to repeat\n
    {% endfor %}
    """
    try:
        fnctn, num, trash, context_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%s takes the syntax %s number_to_iterate\
as context_variable" % (fnctn, fnctn))
    if not trash == 'as':
        raise template.TemplateSyntaxError("%s takes the syntax %s number_to_iterate\
            as context_variable" % (fnctn, fnctn))
    return RangeNode(num, context_name)


# region [ Var Dumps ]
def _clean_type_and_class(obj_type):
    cleaned = str(obj_type).replace('class ', '').replace('\'', '')
    full_name = cleaned.strip('<>')
    short_name = full_name.split('.')[-1]

    return '<span class="object-type" title="{full_name}">{short_name}<span>'\
        .format(full_name=escape(full_name), short_name=escape(short_name))


def _dump(var_name, object, show_functions, depth):
    """
    Recursive var_dumps func

    :param object:
    :param show_functions: 0=> no function, 1=> show dunder, 2=> no dunder, 3=> show only non-builded-in func
    :param depth:
    :return:
    """
    name_to_value = OrderedDict()

    header = '<div class="row"><div class="col-md-6 col-sm-12"><<h1>{name} <{class_name}></h1><table class="table var_dumps"><thead><tr><th scope="col">Name</th><th scope="col">Type</th><th scope="col">Value</th></tr></thead>\n'\
        .format(name=escape(var_name), class_name=_clean_type_and_class(object.__class__))
    body = '<tbody>\n'

    if show_functions:
        for attr_name in dir(object):
            if show_functions >= 2 and attr_name.startswith('_'):
                continue

            attr = Obj.getattr(object, attr_name, execute_callable=False)
            if show_functions >= 3 and isinstance(attr, BuiltinFunctionType):
                continue

            name_to_value[attr_name] = attr

    properties_dict = Obj.get_dict(object)
    name_to_value.update(properties_dict)

    for attr_name, attr in name_to_value.items():
        attr_type_name = _clean_type_and_class(type(attr))
        body += '\t<tr><td scope="row">{name}</td><td>{type}</td><td>{value}</td></tr>\n'.format(name=escape(attr_name), type=attr_type_name, value=escape(attr))
    body += '</tbody></table></div></div>\n'

    return mark_safe(header + body)


@register.simple_tag
def var_dumps(var_name, object, show_functions=3, depth=3):
    """
    Display the function and
    :param object:
    :param show_functions:
    :return:
    """
    return _dump(var_name, object, int(show_functions), depth)

# endregion