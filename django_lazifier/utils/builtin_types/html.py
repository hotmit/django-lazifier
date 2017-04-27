from django.template import defaultfilters
from django.utils.safestring import mark_safe
from django_lazifier.utils.builtin_types.list import Lst
from django_lazifier.utils.builtin_types.str import Str


class Html:
    @classmethod
    def _make_attr(cls, attr, value, is_clean_value=False):
        if not value:
            return ''
        value = value if is_clean_value else defaultfilters.escape(value)
        return mark_safe(' %s="%s"' % (Str.to_css_id(attr), value))

    @classmethod
    def get_class_tag_string(cls, css_classes: list):
        return cls._make_attr('class', cls.get_classes_string(css_classes), True)

    @classmethod
    def get_id_tag_string(cls, css_id: str, id_prefix=''):
        if id_prefix:
            id_prefix = id_prefix.strip('-') + '-'
        return mark_safe(cls._make_attr('id', Str.to_css_id(id_prefix + css_id)))

    @classmethod
    def gen_attr_tags(cls, attr_dict: dict):
        """
        Return the the string of all the attributes (ie. ' attr1="value1" attr2="value2"')

        :param attr_dict:
        :return:
        """
        result = ''
        if attr_dict:
            for k, v in attr_dict.items():
                if k.lower() in ['disabled', 'readonly', 'checked']:
                    result += ' %s' % k.lower()
                else:
                    result += ' %s="%s"' % (Str.snake_to_kebab(k), defaultfilters.escape(v))
        return mark_safe(result)

    @classmethod
    def gen_data_tags(cls, data_dict: dict):
        """
        Return the the string of all data (ie. ' data-key1="value1" data-key2="value2"')

        :param data_dict:
        :return:
        """
        result = ''
        if data_dict:
            for k, v in data_dict.items():
                result += ' data-%s="%s"' % (Str.snake_to_kebab(k), defaultfilters.escape(v))
        return  mark_safe(result)

    @classmethod
    def get_classes_string(cls, css_classes: list):
        """
        Return unique class string (without "class" attribute)

        :param css_classes:
        :return:
        """
        if not css_classes:
            return ''
        css_classes = map(lambda itm: defaultfilters.escape(itm.strip()), css_classes)
        css_classes = filter(lambda itm: itm, css_classes)
        css_classes = Lst.get_unique(css_classes)

        if not css_classes:
            return ''

        return mark_safe(' '.join(css_classes).strip())


class HtmlTag:
    @property
    def id_tag_string(self):
        return Html.get_id_tag_string(self.css_id, self.css_id_prefix)

    @property
    def attr_tags_string(self):
        return Html.gen_attr_tags(self.html_attrs)

    @property
    def data_tags_string(self):
        return Html.gen_data_tags(self.html_data)

    @property
    def css_classes_string(self):
        return Html.get_classes_string(self.css_classes)

    @property
    def class_tag_string(self):
        return Html.get_class_tag_string(self.css_classes)

    @property
    def tags_string(self):
        """
        All in one tags string (id, css_classes, data, attrs)

        :return:
        """
        return mark_safe('{id}{classes}{data}{attrs}'.format(id=self.id_tag_string, classes=self.class_tag_string,
                                                             data=self.data_tags_string, attrs=self.attr_tags_string))

    @property
    def css_classes(self):
        return self._css_classes

    @css_classes.setter
    def css_classes(self, value):
        self._css_classes = value

    def __init__(self, css_id=None, css_id_prefix='', css_classes: list = None, data: dict = None, attrs: dict = None):
        self._css_classes = []

        self.css_id = css_id or ''
        self.css_id_prefix = css_id_prefix
        self.css_classes = css_classes or []
        self.html_data = data or {}
        self.html_attrs = attrs or {}

    def add_css_classes(self, *classes):
        if classes:
            classes = list(filter(lambda c: c, classes))
            self.css_classes += classes


class ColumnTag(HtmlTag):
    @property
    def col_class_list(self):
        result = []
        col_offset_class = '%soffset-%s' % (self.col_offset, self.col_offset) if self.col_offset else ''
        col_size_class = '%s%s' % (self.col_class, self.col_size)

        if self.col_class and self.col_size:
            result.append(col_size_class)

        if col_offset_class:
            result.append(col_offset_class)

        return result

    def __init__(self, *args, col_size, col_class='col-md-', col_offset=0, **kwargs):
        super().__init__(*args, **kwargs)

        self.col_size = col_size
        self.col_class = col_class
        self.col_offset = col_offset

        self.add_css_classes(*self.col_class_list)
