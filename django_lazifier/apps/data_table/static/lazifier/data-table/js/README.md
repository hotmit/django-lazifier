# Css Class
* .btn-dt-create
* .btn-dt-edit
* .btn-dt-delete
* .dt-action-btn.dt-modal-dialog
    * Fetch the remote modal form and display it
    * The result must be wrapped in ".dt-ajax-container form"
    * Data: $btn.data(), 'mode: custom', GET
* .dt-action-btn.dt-action-command
    * Submit a command
    * Data: $btn.data(), 'mode: custom', POST, CSRF

    