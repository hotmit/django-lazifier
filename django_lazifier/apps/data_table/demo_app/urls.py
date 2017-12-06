from django.conf.urls import url
from . import views
from django_lazifier.apps.data_table.demo_app.demo_data import generate_sample_data

urlpatterns = [
    url(r'^$', views.view_demo_app, name='view_demo_app'),
    url(r'^manage/$', views.semi_auto_manual_param_override__manage_demo_app, name='manage_demo_app'),

    # ignore url below
    url(r'^gen-data/$', generate_sample_data, name='generate_sample_data'),
]
