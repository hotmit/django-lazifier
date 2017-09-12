import copy
from crispy_forms.layout import Div, Field
from django import forms
from django.conf import settings
from collections import OrderedDict
from django.forms import ModelForm, Form
from django.shortcuts import render
from django_lazifier.utils.builtin_types.dict import DefaultOrderedDict
from django_lazifier.utils.builtin_types.iter import index_iter
from django_lazifier.utils.builtin_types.obj import Obj
from django_lazifier.utils.builtin_types.request import Rqst
from django_lazifier.utils.utils import p
from django.utils.translation import ugettext as _
from django.db.models import Model


class Frm:
    @classmethod
    def _get_form_kwargs(cls, form_kwargs: dict):
        result = OrderedDict()
        for k, v in form_kwargs.items():
            if k.startswith('form__'):
                result[k[5:]] = v
            else:
                result[k] = v
        return result

    @classmethod
    def process_ajax_new_form(cls, request, form_class, permission, *form_args, form_template=None, form_data=None,
                              **form_kwargs):
        if not request.user.has_perm(permission):
            return render(request, 'data_table/data_table_html_content.html',
                          {'result': _('Sorry, you do not have the permission to view this page.')})

        reset_form = Rqst.get_post_get_param(request, 'submit-via', '') == 'ajax-reset'
        template = form_template or 'data_table/data_table_form_view.html'

        if request.method == 'GET' or reset_form:
            form = form_class(*form_args, **form_kwargs)
            return render(request, template, {'dt_tbl': {'form': form}})

        form_data = form_data or request.POST
        form_kwargs = cls._get_form_kwargs(form_kwargs)
        form = form_class(*form_args, data=form_data, files=request.FILES, **form_kwargs)
        if form.is_valid():
            return form

        return render(request, template, {'dt_tbl': {'form': form}})

    @classmethod
    def process_ajax_update_form(cls, request, form_class, permission, model: Model, *form_args, form_data=None,
                                 form_template=None, instance_filter: dict = None, **form_kwargs):
        if not request.user.has_perm(permission):
            return render(request, 'data_table/data_table_html_content.html',
                          {'result': _('Sorry, you do not have the permission to view this page.')})

        reset_form = Rqst.get_post_get_param(request, 'submit-via', '') == 'ajax-reset'
        template = form_template or 'data_table/data_table_form_view.html'

        form_data = form_data or request.POST
        form_kwargs = cls._get_form_kwargs(form_kwargs)
        pk_filter = instance_filter or {'pk': Rqst.get_pk_or_id(request)}
        instance = form_kwargs.pop('instance', model.objects.filter(**pk_filter).first())

        if not instance:
            return render(request, 'data_table/data_table_html_content.html',
                          {'result': _('Sorry, the record you specified does not exist.')})

        if request.method == 'GET' or reset_form:
            form = form_class(*form_args, instance=instance, **form_kwargs)
            return render(request, template, {'dt_tbl': {'form': form}})

        form = form_class(*form_args, data=form_data, files=request.FILES, instance=instance, **form_kwargs)
        if form.is_valid():
            return form

        return render(request, template, {'dt_tbl': {'form': form}})

    @classmethod
    def get_search_form(cls, form, data, **form_kwargs):
        """
        :rtype: type(form)
        """
        if data:
            filter_form = form(data=data, **form_kwargs)
            if filter_form.is_valid():
                return True, filter_form
            return False, filter_form

        search_form = form(**form_kwargs)
        return False, search_form

    @classmethod
    def get_initial(cls, data, form: ModelForm, prefix=''):
        """
        Extract data from post to put it in form.initial

        :param data: dict|request.GET|request.POST|request.REQUEST
        :param form:
        :param prefix:
        :return:
        """
        if not data:
            return OrderedDict()

        data = Obj.get_dict(data)
        if prefix:
            # the Form put a dash between the prefix and the name
            # eg. field=name, prefix=alert  it becomes alert-name
            prefix += '-'

        result = OrderedDict()
        fields = list(form.base_fields.keys())

        for k, v in data.items():
            if not prefix or k.startswith(prefix):
                k = k.replace(prefix, '')

                if k in fields:
                    result[k] = v
        return result

    @classmethod
    def order_fields(cls, form_instance, field_list: list):
        """
        Reorder the fields based on the specified list (skip if not in the current field)

        :type form_instance: Form|ModelForm
        :param form_instance:
        :param field_list:
        :return:
        """
        not_in_list = OrderedDict([(key, field)
                                            for key, field in form_instance.fields.items() if key not in field_list])

        fields = OrderedDict([(f, form_instance.fields[f])
                              for f in field_list
                              if f in form_instance.fields])
        fields.update(not_in_list)
        form_instance.fields = fields

    @classmethod
    def set_flow_layout(cls, form, layout_definitions, strict=False):
        """

        Example Layout Definitions:
            definitions = [
                'email',
                ['first_name', 'last_name', ''],    # one emptied
                ['two', 'field'],
                ['city', 'prov', 'postal'],
            ]

        :type layout_definitions: list|None
        :param form: the form instance
        :param layout_definitions: the definition for the order and the layout
        :param strict: if true, ignore form fields order, strictly follow specified layout_definitions (ie. if it
            not listed in the definition it doesn't show)
        """

        if not layout_definitions or not form.fields:
            return

        if strict is False:
            helper_layout = None
            if layout_definitions:
                layout = DefaultOrderedDict(list)
                for fn, f in form.fields.items():
                    added = False
                    for row, index0 in index_iter(layout_definitions):
                        if isinstance(row, list):
                            if fn in row:
                                layout[index0].append(fn)
                                added = True
                                break
                        elif fn == row:
                            # single field name as a string
                            layout[fn] = fn
                            added = True
                            break
                    if not added:
                        layout[fn] = fn

                if layout:
                    helper_layout = []
                    for k, v in layout.items():
                        if isinstance(v, list):
                            bs_col_value = 12 / len(layout_definitions[int(k)])
                            bs_col_class = 'col-sm-%d' % bs_col_value
                            fields = map(lambda field_name: Div(field_name, css_class=bs_col_class), v)
                            helper_layout.append(Div(*fields, css_class='row'))
                        else:
                            helper_layout.append(Field(v))
                    helper_layout = Div(*helper_layout)

                if helper_layout:
                    form.helper.layout = helper_layout
        else:
            helper_layout = []
            for hidden_field in form.hidden_fields():
                helper_layout.append(Field(hidden_field.name))

            for row in layout_definitions:
                if isinstance(row, list):
                    row_fields = filter(lambda field_name: field_name in form.fields, row)
                    bs_col_value = 12 / len(row)
                    bs_col_class = 'col-sm-%d' % bs_col_value
                    fields = map(lambda field_name: Div(field_name, css_class=bs_col_class), row_fields)
                    helper_layout.append(Div(*fields, css_class='row'))
                else:
                    if row in form.fields:
                        helper_layout.append(Div(row))

            if helper_layout:
                helper_layout = Div(*helper_layout)
                form.helper.layout = helper_layout

    @classmethod
    def is_valid_choice(cls, form_instance, field_name, value=None):
        """
        Determine if the value is a valid field choice value. If value is None use the field data from the form.

        :type form_instance: Form|ModelForm
        :param form_instance:
        :param field_name:
        :param value:
        :return:
        """
        try:
            if value is None:
                value = form_instance.data.get(field_name, None)

            for k, v in form_instance.fields[field_name].choices:
                if k == value:
                    return True
        except Exception as ex:
            if settings.DEBUG:
                p('Exception: %s' % ex)
            return False
        return False

    @classmethod
    def set_as_required(cls, form_instance, field_list: list=None):
        """
        Make all the specified fields as required.

        :type form_instance: Form|ModelForm
        :param form_instance:
        :param field_list:  if None, make all fields as required
        :return:
        """
        for fn, field in form_instance.fields.items():
            if field_list is None or fn in field_list:
                field.required = True

    @classmethod
    def set_as_readonly(cls, form_instance, field_list: list=None):
        """
        Make all the specified fields as readonly (readonly display text and still submit with the form).
        *** Remember to add the display "Select" fields to your layout. (ie <readonly_field>_display)

        :type form_instance: Form|ModelForm
        :param form_instance:
        :param field_list:  if None, make all fields as readonly.
        """

        display_fields = {}

        for fn, field in form_instance.fields.items():
            if field_list is None or fn in field_list:
                if isinstance(field.widget, forms.Select):
                    try:
                        display_field = copy.copy(field)
                        display_field.widget = forms.TextInput(attrs=field.widget.attrs)

                        # "disabled" is not a typo, disable only display the text but not submit with the form
                        display_field.widget.attrs['disabled'] = True

                        value = Frm.get_data_or_initial(form_instance, fn, display_field.initial)
                        choices = dict(display_field.choices)
                        if value in choices:
                            value = choices[value]
                        display_field.initial = value
                        display_field.required = False

                        display_fields[fn] = display_field

                        field.widget = forms.HiddenInput()
                    except Exception as ex:
                        print('Error: %s' % ex)
                else:
                    field.widget.attrs['readonly'] = True

        if display_fields:
            new_fields = OrderedDict()
            for fn, field in form_instance.fields.items():
                new_fields[fn] = field

                if fn in display_fields:
                    new_fields['%s_display' % fn] = display_fields[fn]
            form_instance.fields = new_fields

    @classmethod
    def set_as_disabled(cls, form_instance, field_list: list=None):
        """
        Make all the specified fields as disabled (disabled display text but doesn't
        submit with the form, ie so data on server side).

        :type form_instance: Form|ModelForm
        :param form_instance:
        :param field_list:  if None, make all fields as readonly
        """
        for fn, field in form_instance.fields.items():
            if field_list is None or fn in field_list:
                field.widget.attrs['disabled'] = True

    @classmethod
    def set_widget_class(cls, form_instance, field_list: list=None, css_class: str = ''):
        """
        Assign css class to the specified field_list

        :param css_class: assign the specified classes string
        :type form_instance: Form|ModelForm
        :param form_instance:
        :param field_list:
        """
        for fn, field in form_instance.fields.items():
            if field_list is None or fn in field_list:
                field.widget.attrs['class'] = css_class

    @classmethod
    def get_data_or_initial(cls, form_instance, field_name: str, default_value=None, to_int=False):
        """
        Get value from data first, if not found then get it from the form initial value.

        :type form_instance: Form|ModelForm
        :param form_instance:
        :param field_name:
        :param default_value:
        :param to_int: set to true to convert the result to int
        :return:
        """
        try:
            if form_instance.data and field_name in form_instance.data:
                result = form_instance.data.get(field_name, None)
                if result is not None:
                    if to_int:
                        return int(result)
                    return result

            if form_instance.initial and field_name in form_instance.initial:
                result = form_instance.initial.get(field_name, default_value)
                if to_int:
                    return int(result)
                return result

            return default_value
        except Exception as ex:
            if settings.DEBUG:
                p('Exception: %s' % ex)
            return default_value

    @classmethod
    def stage_audit_dict(cls, form):
        """
        Call the model default 'get_audit_dict()' function to prepare for the audit stage data.

        :type form: Form|ModelForm
        :param form:
        """
        instance = Obj.getattr(form, 'instance', None)
        if instance and instance.pk and Obj.has_func(instance, 'get_audit_dict'):
            instance._staged_data_point = instance.get_audit_dict()
# endregion
