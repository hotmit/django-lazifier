from django.template import defaultfilters
from django_lazifier.utils.builtin_types.html import Html


class DtActionButton:

    @property
    def attr_string(self):
        return Html.gen_attr_tags(self.attrs)

    @property
    def data_string(self):
        return Html.gen_data_tags(self.data)

    @property
    def css_classes_string(self):
        css_classes = self.css_classes

        if self.button_css:
            css_classes += [self.button_css]

        if self.modal_dialog:
            css_classes += ['dt-modal-dialog']
        elif not self.is_link:
            css_classes += ['dt-action-command']
        return Html.get_classes_string(css_classes)

    def __init__(self, button_text, command, permission, icon_class, add_css_classes: list=None, modal_dialog=False,
                 bs_dialog_title='', is_link=False, link_url='', attrs=None, can_display=None, get_link=None,
                 button_css='btn btn-primary btn-xs', js_confirm=False, js_confirm_msg=None, js_data_formatter=None,
                 **data):
        """
        See data_table/README.md
        """

        self.css_classes = []
        if not is_link:
            self.css_classes += ['dt-action-btn']

        self.button_text = button_text
        self.permission = permission
        self.icon_class = icon_class
        self.modal_dialog = modal_dialog
        self.is_link = is_link
        self.link_url = link_url
        self.button_css = button_css

        if add_css_classes:
            self.css_classes += add_css_classes

        self.id_attr = 'id="dt-action-btn-%s"' % defaultfilters.escape(command)

        self.attrs = attrs or {}

        self.data = data or {}
        self.data.update({
            'command': command,
            'bs_dialog_title': bs_dialog_title,
        })

        if js_data_formatter:
            self.data['data_formatter'] = js_data_formatter

        if js_confirm:
            self.data['confirm'] = 'yes'
            if js_confirm_msg:
                self.data['confirm_msg'] = js_confirm_msg

        self.can_display_button_func = can_display
        self.get_link_func = get_link

    def can_display_button(self, row):
        if self.can_display_button_func is not None:
            return self.can_display_button_func(self, row)
        return True

    def get_link(self, row):
        if self.get_link_func is not None:
            return self.get_link_func(self, row)
        return self.link_url


class DtTableData:
    """
    Set data in the table element.
    """

    @property
    def data_string(self):
        return Html.gen_data_tags(self.data)

    def __init__(self, bs_dialog_size='size-normal', bs_dialog_type='type-primary', **data):
        """

        :param args:
        :param bs_dialog_size: BootstrapDialog.SIZE_NORMAL | .SIZE_WIDE  | .SIZE_LARGE
        | size-normal | size-wide | size-large
        :param kwargs:
        :return:
        """
        if bs_dialog_size != 'size-normal':
            data.update({
                'bs_dialog_size': bs_dialog_size,
            })

        if bs_dialog_type != 'type-primary':
            data.update({
                'bs_dialog_type': bs_dialog_type,
            })

        self.data = data
