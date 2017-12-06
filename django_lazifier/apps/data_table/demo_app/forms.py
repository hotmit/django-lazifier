from django import forms
from django_lazifier.apps.data_table.demo_app.models import DemoModel
from django_lazifier.apps.data_table.forms import DataTableCreateForm, DataTableUpdateForm


class DemoAppCreateForm(DataTableCreateForm):
    class Meta:
        model = DemoModel
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['gender'].widget = forms.RadioSelect()


class DemoAppUpdateForm(DemoAppCreateForm, DataTableUpdateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
