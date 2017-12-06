from enum import Enum
from django.db.models import Model
from django.forms import Form
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django_lazifier.apps.data_table.data_table import DataTablePermissions
from django_lazifier.utils.builtin_types.enum import Enm
from django_lazifier.utils.builtin_types.str import Str
from django_lazifier.utils.django.ajax import Ajx


class FormMode(Enum):
    create = 'create'
    update = 'update'
    delete = 'delete'
    custom = 'custom'


class DataTableManager(DataTablePermissions):
    request = None

    context = {
        'dt_tbl': {
            'perms': {
                'can_view': False,
                'can_create': False,
                'can_update': False,
                'can_delete': False,
                'can_manage': False,    # manage => view, update, and delete
            },
        }
    }

    # region [ Properties ]
    model = Model
    form_template_name = 'data_table/data_table_form_view.html'
    error_response = None

    # region [ Init Vars ]
    create_form = None
    update_form = None
    dom_refresh_selector = None
    mode = FormMode.create
    # endregion

    # region [ Override Params ]
    override_param_id = None    # the ?id for update or delete
    """
    Set your own primary key value.
    """

    override_instance = None    # the instance specified by the ?id in the GET
    """
    Set your own instance for update and delete. Make sure it is the same type as DataTableManager.model
    """

    override_form = None        # the create or update form
    """
    Set your own create or delete form.
    """
    # endregion

    # region [ Override Functions ]
    override_on_create = None
    """
    Create a new instance. To return an error message set the error on the form and return False in the function.

    override_on_create(dtm: DataTableManager, form): bool
    default: form.save()
    """

    override_on_update = None
    """
    Update the form. To return an error message set the error on the form and return False in the function.

    override_on_update(dtm: DataTableManager, form): bool
    default: form.save()
    """

    override_on_delete = None
    """
    Perform the delete on the supplied instance. To return an error message, throw an exception
    to return a message to the user.

    override_on_delete(dtm: DataTableManager, instance): void
    default: instance.delete()
    """

    on_custom_action = None
    """
    Return custom action ?mode==action, command==command_text
    on_custom_action(dtm: DataTableManager, instance, command): void
    """
    # endregion

    @property
    def i18n(self):
        """
        Change any international phrase.

        Usage: dtm.i18n['no_record_found'] = _('Not thing to see here, go away ...')

        'i18n': {
                'no_record_found': _('The record you specified does not exist.'),
                'no_perm_to_create': _('Sorry, you do not have the permission to create this record.'),
                'no_perm_to_update': _('Sorry, you do not have the permission to update this record.'),
                'no_perm_to_delete': _('Sorry, you do not have the permission to delete this record.'),
            },
        :return:
        """
        return self.context['dt_tbl']['i18n']

    # region [ Standard Response ]
    _no_records_found_response = None

    @property
    def no_records_found_response(self):
        if self._no_records_found_response is None:
            msg = str(self.i18n['no_record_found'])
            return Ajx.send_ajax_command(msg,
                                         display_method=Ajx.DisplayMethod.bs_dialog,
                                         status=Ajx.Status.error)
        return self._no_records_found_response

    @no_records_found_response.setter
    def no_records_found_response(self, value):
        self._no_records_found_response = value

    _success_response = None

    @property
    def success__ajax_refresh_response(self):
        if self._no_records_found_response is None:
            return Ajx.send_ajax_command(display_method=Ajx.DisplayMethod.none,
                                             command=Ajx.Command.ajax_refresh,
                                             common_target=self.dom_refresh_selector,
                                             js_on_ajax_success='DTbl.refreshDataTable')
        return self._success_response

    @success__ajax_refresh_response.setter
    def success__ajax_refresh_response(self, value):
        self._success_response = value
    # endregion
    # endregion

    def __init__(self, request, model: model, create_form, update_form, ajax_refresh_selector='.dt-list-view'):
        """
        :param request: the request object
        :param model: the model use in this manager
        :type create_form: Form|ModelForm
        :param create_form: the create form
        :type update_form: Form|ModelForm
        :param update_form: the update form
        :param ajax_refresh_selector: jQuery selector for ajax refresh
                                        (ie this region will be refresh using ajax method)
        """

        super().__init__()

        self.context = {
            'dt_tbl': {
                'perms': {
                    'can_create': False,
                    'can_update': False,
                    'can_delete': False,
                    'can_manage': False,    # manage => can create, update, and delete
                },
                'i18n': {
                    'no_record_found': _('The record you specified does not exist.'),
                    'no_perm_to_create': _('Sorry, you do not have the permission to create this record.'),
                    'no_perm_to_update': _('Sorry, you do not have the permission to update this record.'),
                    'no_perm_to_delete': _('Sorry, you do not have the permission to delete this record.'),
                },
            }
        }

        self.request = request
        self.model = model
        self.create_form = create_form
        self.update_form = update_form
        self.dom_refresh_selector = ajax_refresh_selector

        self.reset_form = request.POST.get('submit-via', request.GET.get('submit-via', '')) == 'ajax-reset'
        mode = request.POST.get('mode', request.GET.get('mode', 'create'))
        self.mode = Enm.from_value(FormMode, mode, FormMode.create)

        self.command = request.POST.get('command', request.GET.get('command', None))

    def is_custom_command(self, command):
        return self.mode == FormMode.custom and self.command == command

    def get_param_id(self):
        """
        Extract the id from request or override_param_id if specified
        :return:
        """
        if self.override_param_id is None:
            param_id = Str.int_val(self.request.GET.get('id', self.request.POST.get('id', None)), None)
            return param_id
        return self.override_param_id

    def get_create_form(self, *args, **kwargs):
        """
        Initialize the create_form or return the override_form if specified.
        :param args: form args
        :param kwargs: form kwargs
        :return: the initialized form
        """
        if self.override_form is None:
            return self.create_form(*args, **kwargs)
        return self.override_form

    def get_update_form(self, *args, **kwargs):
        """
        Initialize the update_form or return the override_form if specified.
        :param args: form args
        :param kwargs: form kwargs
        :return: the initialized form
        """
        if self.override_form is None:
            return self.update_form(*args, **kwargs)
        return self.override_form

    def get_instance(self):
        """
        Get the instance of the model specified by the param_id or
        return override_instance if specified.

        :return: instance of current model
        """
        if self.override_instance is None:
            param_id = self.get_param_id()
            return self.model._default_manager.filter(pk=param_id).first()
        return self.override_instance

    def return_no_permission_message(self, permission_message_key: str):
        """
        Return no permission message via ajax_command.

        :param permission_message_key: eg. no_perm_to_view
        :return: HttpResponse|AjaxCommand
        """
        message = self.i18n[permission_message_key]
        return Ajx.send_ajax_command(message,
                                         display_method=Ajx.DisplayMethod.bs_dialog,
                                         status=Ajx.Status.error)

    def render_response(self, *form_args, **form_kwargs):
        """
        Render and return the response based on the mode and the input.

        :param form_args: form args
        :param form_kwargs: form kwargs
        :return: HttpResponse
        """
        try:
            if self.mode == FormMode.create:
                if not self.perms['can_create'] and not self.perms['can_manage']:
                    return self.return_no_permission_message('no_perm_to_create')

                if self.request.method == 'GET' or self.reset_form:
                    form = self.get_create_form(*form_args, **form_kwargs)
                    return self.render_form(form)

                form = self.get_create_form(data=self.request.POST, files=self.request.FILES, *form_args, **form_kwargs)
                if form.is_valid():
                    result = True
                    if self.override_on_create is None:
                        form.save()
                    else:
                        result = self.override_on_create(self, form)

                    if result is not False:
                        return self.success__ajax_refresh_response
                # form contains error, return form with validation messages
                return self.render_form(form)

            else:
                instance = self.get_instance()
                if not instance:
                    return self.no_records_found_response

                if self.mode == FormMode.update:
                    if not self.perms['can_update'] and not self.perms['can_manage']:
                        return self.return_no_permission_message('no_perm_to_update')

                    form_kwargs.update({
                        'instance': instance,
                    })
                    default_initial = {
                        'id': instance.pk,
                    }
                    if 'initial' in form_kwargs:
                        form_kwargs['initial'].update(default_initial)
                    else:
                        form_kwargs['initial'] = default_initial

                    if self.request.method == 'GET' or self.reset_form:
                        form = self.get_update_form(*form_args, **form_kwargs)
                        return self.render_form(form)

                    form = self.get_update_form(self.request.POST, self.request.FILES, *form_args, **form_kwargs)
                    if form.is_valid():
                        result = True
                        if self.override_on_update is None:
                            form.save()
                        else:
                            result = self.override_on_update(self, form)

                        if result is not False:
                            return self.success__ajax_refresh_response
                    # form contains error, return form with validation messages
                    return self.render_form(form)

                elif self.mode == FormMode.delete:
                    if not self.perms['can_delete'] and not self.perms['can_manage']:
                        return self.return_no_permission_message('no_perm_to_delete')

                    if self.override_on_delete is None:
                        instance.delete()
                    else:
                        self.override_on_delete(self, instance)

                    return self.success__ajax_refresh_response

                elif self.mode == FormMode.custom and self.on_custom_action is not None:
                    result = self.on_custom_action(self, instance, self.command)

                    if result is True:
                        return self.success__ajax_refresh_response
                    return result
                else:
                    return render(self.request, 'data_table/data_table_html_content.html', {
                        'result': _('Dev Error: un-implemented mode or command ({mode}/{command})').format(
                            mode=self.mode, command=self.command
                        ),
                    })
        except Exception as ex:
            return Ajx.send_ajax_command('Exception: %s' % ex, display_method=Ajx.DisplayMethod.bs_dialog,
                                         status=Ajx.Status.error)

    def render_form(self, form):

        self.context['dt_tbl'].update({
            'form': form,
        })

        return render(self.request, self.form_template_name, self.context)
