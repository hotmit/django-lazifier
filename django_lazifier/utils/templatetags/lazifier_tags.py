from django import template


class AssignNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def render(self, context):
        context[self.name] = self.value.resolve(context, True)
        return ''


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


register = template.Library()
register.tag('assign', assign)
register.tag('range', tag_range)
