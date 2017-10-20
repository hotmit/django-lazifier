from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from datetime import timedelta
from django import forms
from django.utils.translation import ugettext as _
from django.utils import timezone
from django_lazifier.utils.builtin_types.request import Rqst
from django_lazifier.utils.contants.choices import STATUS_ALL_CHOICES
from django_lazifier.utils.django.form import Frm


class DataTableBaseForm(forms.Form):

    strict_flow_layout = False
    flow_layout = None

    class Media:
        js = ('lazifier/data-table/js/initialize-controls.js',)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        if not hasattr(self, 'request'):
            self.request = request

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    def setup_flow_layout(self):
        Frm.set_flow_layout(self, self.flow_layout, strict=self.strict_flow_layout)


class DataTableBaseFilterForm(DataTableBaseForm):

    class Media:
        js = ('lazifier/data-table/js/initialize-search-controls.js',)

    def __init__(self, *args, select_all: list=(), **kwargs):
        """

        """
        super().__init__(*args, **kwargs)
        self.helper.form_method = 'get'
        self.helper.form_class += ' dt-filter-form form-inline'
        self.helper.add_input(Submit('submit', _('Search')))

        for sa in select_all:
            self.select_all(sa)

    def _filter_with_condition(self, queryset, field_name, value, operator='__gte'):
        condition = {
            '%s%s' % (field_name, operator): value
        }
        return queryset.filter(**condition)

    def select_all(self, field_name):
        choices = self.fields[field_name].choices
        self.fields[field_name].initial = list(dict(choices).keys())

    def filter(self, queryset, **kwargs):
        return queryset


class DateRangeFilterForm(DataTableBaseFilterForm):
    start_date = forms.DateField(label=_('Start Date'))
    end_date = forms.DateField(label=_('End Date'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'start_date' not in self.initial:
            self.initial['start_date'] = timezone.now().date() - timedelta(days=30)

        if 'end_date' not in self.initial:
            self.initial['end_date'] = timezone.now().date() + timedelta(days=1)

    def filter_start_date(self, queryset, date_field_name):
        condition = {
            '%s__gte' % date_field_name: self.cleaned_data['start_date']
        }
        return queryset.filter(**condition)

    def filter_end_date(self, queryset, date_field_name):
        condition = {
            '%s__lte' % date_field_name: self.cleaned_data['end_date']
        }
        return queryset.filter(**condition)

    def filter_start_and_end_date(self, queryset, date_field_name):
        result = self.filter_start_date(queryset, date_field_name)
        return self.filter_end_date(result, date_field_name)


class StatusFilterForm(DataTableBaseFilterForm):
    status = forms.ChoiceField(label=_('Status'), choices=STATUS_ALL_CHOICES, initial='all', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def filter_by_status(self, queryset):
        status = self.cleaned_data['status']
        if status == 'all':
            return queryset
        return queryset.filter(status=status)


class DataTableCreateForm(DataTableBaseForm, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        helper = FormHelper()
        helper.form_method = 'POST'
        helper.form_action = 'manage/?mode=create'
        helper.form_id = 'frm-dt-create'
        helper.add_input(Button('ajax-reset', _('Reset'), css_class='btn btn-warning ajax-reset'))
        helper.add_input(Submit('submit', _('Create')))

        self.helper = helper
        self.setup_flow_layout()


class DataTableUpdateForm(DataTableCreateForm):

    id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        helper = FormHelper()
        helper.form_method = 'POST'
        helper.form_action = 'manage/?mode=update'
        helper.form_id = 'frm-dt-update'
        helper.add_input(Button('ajax-reset', _('Reset'), css_class='btn btn-warning ajax-reset'))
        helper.add_input(Submit('submit', _('Update')))

        self.helper = helper
        self.setup_flow_layout()


class DataTableCustomActionForm(DataTableBaseForm):

    id = forms.IntegerField(widget=forms.HiddenInput())
    mode = forms.CharField(initial='custom', widget=forms.HiddenInput)
    command = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

        self.fields['id'].initial = Rqst.get_pk_or_id(request)
        self.fields['command'].initial = Rqst.get_post_get_param(request, 'command', '')

        self.helper.form_action = 'manage/?mode=custom'
        self.setup_flow_layout()
