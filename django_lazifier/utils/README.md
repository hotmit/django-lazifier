## To use the template
* Add **'proj_name.lib'** INSTALLED_APPS in settings.py
* Put this line in the top of the template file **'{% load lib_tags %}'**


## Run test
```
# Run all test
manage.py test proj_name.lib
     
# Run a function test
manage.py test proj_name.lib.test.LstTest
```










# send_ajax_command
