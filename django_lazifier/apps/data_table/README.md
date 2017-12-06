# Requirement
* crispy-form

### Crispy Forms Install
* InstallApp 'crispy_forms',
* Setting CRISPY_TEMPLATE_PACK = 'bootstrap3'
* Optional Setting CRISPY_FAIL_SILENTLY = not DEBUG

# Install
* InstallApp 'django_lazifier',
* InstallApp 'data_table',

# DtActionButton
```
def __init__(self, button_text, command, permission, icon_class, add_css_classes: list=None, modal_dialog=False,
                 bs_dialog_title='', is_link=False, link_url='', attrs=None, can_display=None, get_link=None,
                 button_css='btn btn-primary btn-xs', js_confirm=False, js_confirm_msg=None, **data):

// common
attrs => button attrs
button_css => css class
can_display($btn, $row) => lambda return true to display, false to hide


// form dialog => fetch form => submit()
modal_dialog=True
    // js
    .dt-action-btn.dt-modal-dialog => bs_dialog_title 
        data { id, command }


// run ajax command => submit command => return json
make sure:  modal_dialog is NOT True,   is_link is NOT True
    // optional confirmation
    set js_confirm to True and if you want to customize the message you can use js_confirm_msg  


// regular link no js
is_link => set this to True
link_url => specify the link, if it's a dynamic link use get_link lambda below
get_link($btn, $row) => lambda to generate link on the fly



// js_data_formatter
function <data_formatter_func>($actionButton, $ajaxData){
    return modifiedDataObj;
}
specify the global function name for the ajax function pass the data to before submitting
```