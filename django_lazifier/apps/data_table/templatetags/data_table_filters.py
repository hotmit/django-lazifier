from django import template
from django.template import defaultfilters
from django.utils.safestring import mark_safe
from django_lazifier.apps.data_table.data_table_setting_classes import DtActionButton
from django_lazifier.utils.builtin_types.str import Str
from django_lazifier.utils.templatetags.lazifier_filters import get_attr, apply_filter

register = template.Library()


@register.filter
def make_action_button(obj: DtActionButton, row):
    """
    :param obj: the action button definition
    :param row_id: the current row id
    """
    if not obj:
        return None

    row_id = getattr(row, 'pk', 0)
    row_id_attr = 'data-id="%s"' % row_id

    href = '' if not obj.is_link else ' href="%s"' % defaultfilters.escape(obj.get_link(row))
    element = 'a' if obj.is_link else 'button'

    return mark_safe("""<{element} {id_attr} class="{css_classes}" {row_id_attr}{href}{row_data}{row_attrs}>
            <span class="{icon_class}"></span> <span class="btn-text">{button_text}</span>
        </{element}>""".format(element=element, id_attr=obj.id_attr, css_classes=obj.css_classes_string,
                               row_id_attr=row_id_attr, href=href, row_data=obj.data_string, row_attrs=obj.attr_string,
                               icon_class=obj.icon_class, button_text=obj.button_text))


@register.filter
def can_display_button(obj: DtActionButton, row):
    return bool(obj.can_display_button(row))


@register.filter
def get_dt_col_value(obj, attr: str):
    property, filters = Str.split_parts(attr, '|', 1, [None, None])
    if filters is None:
        return get_attr(obj, attr)
    value = get_attr(obj, property)
    return apply_filter(value, filters)
