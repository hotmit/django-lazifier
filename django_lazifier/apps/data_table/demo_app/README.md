### Usage:
* Add to InstallApps 'data_table.demo_app'
* Add to TemplatePath os.path.join(BASE_DIR, 'data_table/demo_app/templates'),
* Add to url url(r'^data-table/demo/$', include('data_table.demo_app.urls', namespace='demo_app')),
