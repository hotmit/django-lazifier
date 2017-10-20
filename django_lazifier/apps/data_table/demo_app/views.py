from django.utils.translation import ugettext as _
from django_lazifier.apps.data_table.data_table import DataTable
from django_lazifier.apps.data_table.data_table_manager import DataTableManager, FormMode
from django_lazifier.apps.data_table.demo_app.forms import DemoAppCreateForm, DemoAppUpdateForm
from django_lazifier.apps.data_table.demo_app.models import DemoModel
from django_lazifier.utils.builtin_types.str import Str


def view_demo_app(request):
    sample_data = DemoModel.objects.all()

    # region [ Old Ways ]

    # tmplt_data = {
    #     'dt_tbl': {
    #         'options': {
    #             'table_id': '',
    #             'table_classes': '',
    #         },
    #         'styles': {
    #             'view': [],
    #         },
    #         'i18n': {
    #             'not_found': _('No records found.'),
    #             'no_perm_to_view': _('Sorry, you do not have the permission to view this page.'),
    #             'edit': _('Edit'),
    #             'delete': _('Delete'),
    #         },
    #         'perms': {
    #             'can_view': True,
    #             'can_update': False,
    #             'can_delete': False,
    #             'can_manage': True,
    #         },
    #         'data': sample_data,
    #
    #         'display': {
    #             'col_titles': [ _('Name'), _('User'), _('Gender'), _('Pins'), _('Date Modified') ],
    #             'fields': [
    #                 'name', 'user', 'get_gender_display', 'pins', 'modified',
    #             ],
    #             'formats': {
    #
    #             }
    #         }
    #     },
    # }
    #
    # return render(request, 'demo_app/view_demo_app.html', tmplt_data)

    # endregion

    dt = DataTable(request)
    dt.set_permissions({
        'can_view': True,
        # 'can_update': 'demo_app.update_demoapp',
        # 'can_delete': 'demo_app.delete_demoapp',
        'can_manage': True,
    })

    dt.data = sample_data
    dt.col_titles_display = [_('Name'), _('User'), _('Gender'), _('Pins'), _('Date Modified')]
    dt.col_fields_display = ['name', 'user', 'get_gender_display', 'pins', 'modified']

    dt.js_data_table_settings(default_sort_col=2, default_sort_direction='desc', no_sort_cols=[3, 4])

    return dt.render('demo_app/view_demo_app.html')


def full_auto__manage_demo_app(request):
    dtm = DataTableManager(request, DemoModel, DemoAppCreateForm, DemoAppUpdateForm)

    # These should be replace with actual permission name "app_label.permission_name"
    dtm.set_permissions({
        'can_view': False,
        'can_update': False,
        'can_delete': False,
        'can_manage': True,    # manage => view, update, and delete
    })

    return dtm.render_response()


def semi_auto_manual_param_override__manage_demo_app(request):
    dtm = DataTableManager(request, DemoModel, DemoAppCreateForm, DemoAppUpdateForm)

    # override the form template
    dtm.form_template_name = 'demo_app/demo_app_form.html'

    dtm.set_permissions({
        'can_view': False,
        'can_create': False,
        'can_update': False,
        'can_delete': False,
        'can_manage': True,    # manage => view, update, and delete
    })

    if dtm.mode == FormMode.create:
        # override form initialization
        if request.method == 'GET' or dtm.reset_form:
            dtm.override_form = DemoAppCreateForm()
        else:
            dtm.override_form = DemoAppCreateForm(request.POST)
    elif dtm.mode == FormMode.update:
        # override param_id
        dtm.override_param_id = request.GET.get('id', request.POST.get('id', None))
        dtm.override_param_id = Str.int_val(dtm.override_param_id, None)

        # override "instance" selection
        dtm.override_instance = DemoModel.objects.filter(pk=dtm.get_param_id()).first()

        # override form initialization
        if request.method == 'GET' or dtm.reset_form:
            dtm.override_form = DemoAppUpdateForm(instance=dtm.get_instance())
        else:
            dtm.override_form = DemoAppUpdateForm(request.POST, instance=dtm.get_instance())

    elif dtm.mode == FormMode.delete:
        dtm.override_param_id = request.POST.get('id', None)
        # override getting "instance"
        dtm.override_instance = DemoModel.objects.filter(pk=dtm.get_param_id()).first()

    return dtm.render_response()


def semi_auto_manual_function_override__manage_demo_app(request):
    dtm = DataTableManager(request, DemoModel, DemoAppCreateForm, DemoAppUpdateForm)
    dtm.set_permissions({
        'can_view': False,
        'can_create': False,
        'can_update': False,
        'can_delete': False,
        'can_manage': True,    # manage => view, update, and delete
    })

    # region [ create mode ]
    # this can be a def (ie function) or lambda expression
    dtm.override_on_create = lambda dt, form: form.save()
    # endregion

    # region [ update mode ]
    def update(data_table_manager, update_form):
        return update_form.save()
    dtm.override_on_update = update
    # endregion

    # region [ delete form mode ]
    def delete(data_table_manager, instance_from_param_id):
        return instance_from_param_id.delete()
    dtm.override_on_delete = delete
    # endregion

    return dtm.render_response()






