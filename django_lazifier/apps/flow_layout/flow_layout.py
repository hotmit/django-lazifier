import math
from django.db.models import Model
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django_lazifier.utils.builtin_types.html import HtmlTag, ColumnTag
from django_lazifier.utils.builtin_types.obj import Obj
from django_lazifier.utils.builtin_types.param import Prm
from django_lazifier.utils.builtin_types.str import Str
from django_lazifier.utils.django.model import Mdl


class FlowLayout(HtmlTag):
    def __init__(self, *rows, obj, **kwargs):
        self.default_itm_params = Prm.get_prefix_kwargs(kwargs, 'itm_', {})
        self.default_col_params = Prm.get_prefix_kwargs(kwargs, 'col_', {})
        self.default_row_params = Prm.get_prefix_kwargs(kwargs, 'row_', {})

        super().__init__(**kwargs)
        self.obj = obj
        self.rows = rows
        self.add_css_classes('fw-layout')

    def _get_col(self, definition, count_per_row):
        col = None
        col_size = math.floor(12 / count_per_row)

        if isinstance(definition, str) or not definition:
            col = FwCol(FwItm(definition, **self.default_itm_params), col_size=col_size, **self.default_col_params)
        elif isinstance(definition, FwItm):
            col = FwCol(definition, col_size=col_size, **self.default_col_params)
        elif isinstance(definition, FwCol):
            col = definition
        return col

    def render(self):
        contents = []

        for r in self.rows:
            row = None

            if isinstance(r, FwRow):
                row = r
            elif isinstance(r, list):
                cols = list(map(lambda c: self._get_col(c, len(r)), r))
                row = FwRow(*cols, **self.default_row_params)
            else:
                col = self._get_col(r, 1)
                if isinstance(col, FwCol):
                    row = FwRow(col, **self.default_row_params)

            contents.append(row.render(self.obj) if Obj.has_func(row, 'render') else r)
        context = {
            'layout': self,
            'contents': contents,
        }
        return mark_safe(render_to_string('flow_layout/flow_layout.html', context))

    def __str__(self):
        return '<flow-layout row-count="%s" />' % len(self.rows)


class FwRow(HtmlTag):
    def __init__(self, *columns, **kwargs):
        super().__init__(**kwargs)
        self.columns = columns
        self.add_css_classes('row', 'fw-row')

    def render(self, obj):
        contents = []
        for col in self.columns:
            contents.append(col.render(obj) if Obj.has_func(col, 'render') else col)

        context = {
            'row': self,
            'contents': contents,
        }
        return mark_safe(render_to_string('flow_layout/row_layout.html', context))

    def __str__(self):
        return '<row%s />' % self.tags_string


class FwCol(ColumnTag):
    def __init__(self, content, **kwargs):
        super().__init__(**kwargs)
        self.content = content
        self.add_css_classes('fw-column', *self.col_class_list)

    def render(self, obj):
        content = self.content.render(obj) if Obj.has_func(self.content, 'render') else self.content
        context = {
            'col': self,
            'content': content,
        }
        return mark_safe(render_to_string('flow_layout/column_layout.html', context))

    def __str__(self):
        return '<col%s />' % self.tags_string


class FwItm(HtmlTag):
    def _parse_field_name(self):
        fn = self.field_name

        parts = fn.split('|', 1)
        if len(parts) == 2:
            fn = parts[0]
            self.field_name = parts[0]
            self.filter = parts[1]

        parts = fn.split('__')
        if len(parts) == 2:
            self.field_name = parts[0]
            self.label_col_size = int(parts[1])

    @property
    def content_col_size(self):
        return 12 - self.label_col_size

    def __init__(self, field_name: str, field_label=None, label_postfix='', **kwargs):
        """
        :param field_name:
        :param field_label:
        :param kwargs: start with lbl_ to target the label tag, start with ctn_ to target content html tag
        """
        self.field_name = field_name
        self.filter = None
        self.field_label = field_label
        self.label_postfix = label_postfix

        if field_name:
            self._parse_field_name()

            label_params = Prm.get_prefix_kwargs(kwargs, 'lbl_', {
                'css_id': field_name,
                'css_id_prefix': 'lbl',
                'css_classes': ['fw-itm-label'],
            })
            self.label_html = HtmlTag(**label_params)

            content_params = Prm.get_prefix_kwargs(kwargs, 'ctn_', {
                'css_id': field_name,
                'css_id_prefix': 'ctn',
                'css_classes': ['fw-itm-content'],
            })
            self.content_html = HtmlTag(**content_params)

        super().__init__(**kwargs)

        self.add_css_classes('fw-itm')

    def render(self, obj):
        context = {
            'label_postfix': self.label_postfix,
            'itm': self,
        }

        if self.field_name:
            label = ''
            content = Obj.getattr(obj, self.field_name)

            if isinstance(obj, Model):
                content = Mdl.get_display_name(obj, self.field_name, content)

            if self.field_label is None:
                default_label = Str.snake_to_title(self.field_name)
                if isinstance(obj, Model):
                    ver_names = Mdl.get_field_verbose(obj, [self.field_name])
                    verbose_name = ver_names[self.field_name]
                    if verbose_name != self.field_name:
                        label = verbose_name
                label = label or default_label

            context.update({
                'label': label,
                'content': content,
            })

        return mark_safe(render_to_string('flow_layout/item_layout.html', context))

    def __str__(self):
        return '<item field="%s" />' % self.field_name
