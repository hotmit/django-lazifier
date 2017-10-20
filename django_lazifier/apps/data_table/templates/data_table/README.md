# List View

### Expected Input



### Blocks
* dt_command_buttons
    * new button
    * if you want to move the buttons: set options.show_command_buttons=False 
        then include **data_table_command_buttons.html** in your own template
* dt_page_nav_header
    * the top page navigation 
* dt_page_nav_footer
* dt_table
    * the table contains the data
* dt_table_header                   # if override this then don't need to specify col_titles
    * display header                 

* dt_row_display                    # should override this block for non generic row view display 
    * the <td> between the tr and the edit button col

* dt_row_action_button_display
    * render of dt_tbl.display.action_buttons 

* dt_buttons
    * the buttons <td> in the display table
* dt_not_found
    * the not found message, you can override this with a search box or something
* dt_no_perm_to_view
    * can_view is false
    
    
### CSS Class
* dt-table
    * the table for the list view
* dt-page-nav page-nav-header
    * top page nav wrapper div
* dt-page-nav page-nav-footer
    * bottom page nav wrapper div

---

# Form View

### Expected Input
{ 
    'dt_form': form_instance,
}

### Blocks
* dt_form_header (emptied by default)
    * put any script or html above the form
* dt_form 
    * the crispy form
* dt_form_footer (emptied by default)
    * put any script or html below the form

### CSS Class
Template Class
* dt-ajax-form-container
    * wrapper around the form

Form Class
* frm-dt-create
* frm-dt-update