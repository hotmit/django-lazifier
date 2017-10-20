# Form
* Shortcut: dt_form

```python
from django_lazifier.ltgt_ext.apps.data_table.forms import DataTableCreateForm, DataTableUpdateForm


class $MODEL$CreateForm(DataTableCreateForm):
    class Meta:
        model = $MODEL$$END$
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class $MODEL$UpdateForm($MODEL$CreateForm, DataTableUpdateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

```

---
# View
* Shortcut: dt_view
* MODEL_NAME = capitalize(underscoresToCamelCase(APP_NAME))

```python
from django.utils.translation import ugettext as _
from django_lazifier.ltgt_ext.apps.data_table.data_table import DataTable
from django.contrib.auth.decorators import login_required, permission_required
from django_lazifier.ltgt_ext.apps.data_table.data_table_manager import DataTableManager


@login_required
@permission_required(['$APP_NAME$.view_$APP_NAME$'])
def view_$APP_NAME$(request):
    data = $MODEL_NAME$.objects.all()

    dt = DataTable(request)
    dt.set_permissions({
        'can_view': '$APP_NAME$.view_$APP_NAME$',
        'can_manage': '$APP_NAME$.manage_$APP_NAME$',
    })

    dt.data = data
    dt.col_titles_display = [_('Name'), _('User'), _('Gender'), _('Pins'), _('Date Modified')]
    dt.col_fields_display = ['name', 'user', 'get_gender_display', 'pins', 'modified']
    dt.col_formats_display = ['', '', '|floatformat:"-3"', '|floatformat:"-3"', '|naturaltime']
    
    dt.js_data_table_settings()

    return dt.render('default_data_table_list_view.html')


@login_required
@permission_required(['$APP_NAME$.manage_$APP_NAME$'])
def manage_$APP_NAME$(request):
    dtm = DataTableManager(request, $MODEL_NAME$$END$, $MODEL_NAME$CreateForm, $MODEL_NAME$UpdateForm)
    
    dtm.set_permissions({
        'can_view': '$APP_NAME$.view_$APP_NAME$',
        'can_manage': '$APP_NAME$.manage_$APP_NAME$',
    })

    return dtm.render_response()

```

---
# Url
* Shortcut: dt_ful_url
* APP_NAME = snakeCase(URL_NAME)

```python
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$URL_NAME$/$', views.view_$APP_NAME$, name='view_$APP_NAME$'),
    url(r'^$URL_NAME$/manage/$', views.manage_$APP_NAME$, name='manage_$APP_NAME$'),    
]

```