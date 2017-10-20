import warnings
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render
from django.template import Template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django_lazifier.apps.data_table.data_table_setting_classes import DtTableData
from django_lazifier.utils.builtin_types.html import HtmlTag
from django_lazifier.utils.builtin_types.iter import index_iter


class DataTablePermissions(HtmlTag):
    request = AnonymousUser

    context = {
        'dt_tbl': {
            'perms': {
                'can_view': False,
                'can_create': False,
                'can_update': False,
                'can_delete': False,
                'can_manage': False,  # manage => view, update, and delete
            },
        }
    }

    @property
    def perms(self):
        """
        Dictionary of permission (boolean only). Use set_permissions() to assign permission
        'perms': {
            'can_view': False,
            'can_create': False,
            'can_update': False,
            'can_delete': False,
            'can_manage': False,    # manage => view, update, and delete
        },
        :return:
        """
        return self.context['dt_tbl']['perms']

    def has_perm(self, perm):
        if type(perm) is bool:
            return perm
        else:
            return self.request.user.has_perm(perm)

    def set_permissions(self, perms: dict):
        """
        Assign permission to "perms".
        set_permissions({                                   # permission can be bool or permission name
            'can_view': True,
            'can_create': False,
            'can_update': 'user_app.manage_userprofile',    # app_label.permission_name
            'can_delete': bool|perm,
            'can_manage': bool|perm,    # can_manage => Can view, update AND delete,
                                        # this will override the other three permissions
        })
        :param perms: the dictionary of permissions
        """
        if perms:
            for name, perm in perms.items():
                if name in self.perms:
                    self.perms[name] = self.has_perm(perm)


class DataTable(DataTablePermissions):
    context = None

    # region [ Properties ]
    @property
    def options(self):
        """
        'options': {
            'table_id': '',
            'table_classes': '',
            'table_data_attr': {},
            'show_command_buttons': True,  # add new buttons
        },
        :return:
        """
        return self.context['dt_tbl']['options']

    @property
    def table_data_attr(self):
        return self.context['dt_tbl']['options']['table_data_attr']

    @table_data_attr.setter
    def table_data_attr(self, value: DtTableData):
        self.context['dt_tbl']['options']['table_data_attr'] = value

    @property
    def css_media(self):
        """
        Static links for all css files

        'css_media': {
            'all': [ 'my-table/css/screen-and-print-style.css' ],
            'screen': [],
            'print': [],
        }
        """
        return self.context['dt_tbl']['css_media']

    @css_media.setter
    def css_media(self, value):
        """
        Static links for all css files

        'css_media': {
            'all': [ 'my-table/css/screen-and-print-style.css' ],
            'screen': [],
            'print': [],
        }
        """
        self.context['dt_tbl']['css_media'] = value

    @property
    def js_media(self):
        """
        Static links for all js files in the footer of the table.

        'js_media': [ 'my-table/css/file.js' ]
        """
        return self.context['dt_tbl']['js_media']

    @js_media.setter
    def js_media(self, value):
        """
        Static links for all js files in the footer of the table.

        'js_media': [ 'my-table/css/file.js' ]
        """
        self.context['dt_tbl']['js_media'] = value

    @property
    def i18n(self):
        """
        'i18n': {
            'not_found': _('No records found.'),
            'no_perm_to_view': _('Sorry, you do not have the permission to view this page.'),
            'add_new': _('New'),
            'edit': _('Edit'),
            'delete': _('Delete'),
        },
        :return:
        """
        return self.context['dt_tbl']['i18n']

    @property
    def data(self):
        """
        The QuerySet or list of data (ie. the data for the rows)
        :return:
        """
        return self.context['dt_tbl']['data']

    @data.setter
    def data(self, value):
        self.context['dt_tbl']['data'] = value

    @property
    def display(self):
        """
        Which fields to display.

        'display': {
            'col_titles': [ _('Name'), _('User'), _('Gender'), _('Pins'), _('Date Modified') ],
            'fields': [
                'name', 'user', 'get_gender_display', 'pins', 'modified',
            ],
            'formats': {
            }
        }
        :return:
        """
        return self.context['dt_tbl']['display']

    @property
    def col_titles_display(self):
        """
        The columns title on the header of the table

        :return:
        :rtype: list
        """
        return self.display['col_titles']

    @col_titles_display.setter
    def col_titles_display(self, value: list):
        self.display['col_titles'] = value

        if not self.col_formats_display:
            self.col_formats_display = []

    @property
    def col_fields_display(self):
        """
        The display value for each row corresponding to the column titles
        :return:
        :rtype: list
        """
        return self.display['col_fields']

    @col_fields_display.setter
    def col_fields_display(self, value: list):
        self.display['col_fields'] = value

    @property
    def col_formats_display(self):
        """
        Format for each column
        :return:
        :rtype: list
        """
        if self.display['formats']:
            return self.display['formats']
        return [''] * len(self.col_titles_display)

    @col_formats_display.setter
    def col_formats_display(self, value: list):
        if not value:
            value = []

        value_count = len(value)
        col_count = len(self.col_titles_display)

        if value_count == col_count:
            self.display['formats'] = value
        else:
            self.display['formats'] = value + ([''] * (col_count - value_count))

    @property
    def command_buttons_display(self):
        """
        List of all action on the table.

        :return: list of [DtActionButton]
        """
        return self.display['cmd_buttons']

    @command_buttons_display.setter
    def command_buttons_display(self, value: list):
        """
        List of all buttons.

        eg. dt.command_buttons_display = [
                DtActionButton(_('Refund'), 'refund', 'manage_own_seat', 'fa fa-undo',
                               button_css='btn btn-primary btn-sm'),
            ]

        :type value: list of [DtActionButton]
        """
        result = []
        for definition in value:
            if self.has_perm(definition.permission):
                result.append(definition)

        self.display['cmd_buttons'] = result

    @property
    def col_action_buttons_display(self):
        """
        List of all action on the table.

        :return: list of [dict]
        """
        return self.display['action_buttons']

    @col_action_buttons_display.setter
    def col_action_buttons_display(self, value: list):
        """
        List of all buttons.

        eg. dt.col_action_buttons_display = [
                DtActionButton(button_text=_('Transfer'), command='transfer-to-trust',
                               permission='fund_transfer.authorize_transfer',
                               icon_class='glyphicon glyphicon-transfer', modal_dialog=True,
                               bs_dialog_title=_('Transfer Fund'), can_display=lambda dt_btn, row: row.transaction is None)
            ]

            dt.col_action_buttons_display = [
                DtActionButton(button_text=_('Details'), command='view-details', permission='trust_fund.view_trustfund',
                           icon_class='glyphicon glyphicon-transfer', is_link=True,
                           get_link=lambda dt_btn, row: reverse('funding:trust_fund:view_trust_fund_details', args=(row.id,))),
            ]

        :type value: list of [DtActionButton]
        """
        result = []
        for definition in value:
            if self.has_perm(definition.permission):
                result.append(definition)

        self.display['action_buttons'] = result
    # endregion

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # region [ Context ]
        self.context = {
            'dt_tbl': {
                'options': {
                    'table_id': '',
                    'table_classes': '',
                    'table_data_attr': {},
                    'show_command_buttons': True,  # add new buttons
                },
                'js_data_table': {
                    'enable': True,
                    'paging': True,
                    'default_sort': {
                        'column': 0,
                        'direction': 'asc',
                    },
                    'no_search_columns': [],
                    'no_sort_columns': [],
                },
                'css_media': [],
                'js_media': [],
                'i18n': {
                    'not_found': _('No records found.'),
                    'no_perm_to_view': _('Sorry, you do not have the permission to view this page.'),
                    'add_new': _('New'),
                    'edit': _('Edit'),
                    'delete': _('Delete'),
                    'action': _('Actions'),
                },
                'perms': {
                    'can_view': False,
                    'can_create': False,
                    'can_update': False,
                    'can_delete': False,
                    'can_manage': False,  # manage => view, update, and delete
                },
                'data': [],
                'display': {
                    'col_titles': [],
                    'col_fields': [],
                    'formats': None,
                    'action_buttons': [],
                },

                'html': self,
            },
        }
        # endregion

        self.request = request

    def js_data_table_settings(self, enable=True, paging=True, default_order='[[0, "asc"]]',
                               no_search_cols=None, no_sort_cols=None, **kwargs):
        """
        Set the javascript data table preferences

        :type no_search_cols: list|None
        :type no_sort_cols: list|None
        :param enable: enable or disable the js-data-table function
        :param paging: enable pagination
        :param no_search_cols: ignore search on these columns (0-index)
        :param no_sort_cols: disable sort on these columns (0-index)
        :param default_sort_col: the default column when the page load (deprecated, use default_order instead)
        :param default_sort_direction: the direction of the sort (deprecated, use default_order instead)
        :return:
        """

        self.context['dt_tbl']['js_data_table'] = {
            'enable': enable,
            'paging': paging,
            'default_order': default_order,
            'no_search_columns': no_search_cols or [],
            'no_sort_columns': no_sort_cols or [],
        }

        if 'default_sort_col' in kwargs or 'default_sort_direction' in kwargs:
            warnings.simplefilter('default_sort_col and default_sort_direction is '
                                  'being replaced with default_order string', DeprecationWarning)

    def assign_display_format(self, display_field, format_filter):
        """
        Set specific display format for a particular field (see .col_fields_display property)

        :param display_field: the field value specified in .col_fields_display
        :param format_filter: the value you would put in .col_formats_display
        :return:
        """
        for field, index0 in index_iter(self.col_fields_display):
            if field == display_field:
                self.col_formats_display[index0] = format_filter

    def _render(self, as_string, template_name, custom_data=None, **kwargs):
        custom_data = custom_data or {}
        self.context['custom_data'] = custom_data
        self.context.update(kwargs)

        if as_string:
            return mark_safe(render_to_string(template_name, context=self.context, request=self.request))
        return render(self.request, template_name, self.context)

    def render(self, template_name, custom_data=None, **kwargs):
        """
        :param custom_data:
        :type template_name: Template|str
        :param template_name: list view template name
        :return:
        """
        return self._render(as_string=False, template_name=template_name, custom_data=custom_data, **kwargs)

    def render_to_string(self, template_name, custom_data=None, **kwargs):
        return self._render(as_string=True, template_name=template_name, custom_data=custom_data, **kwargs)

