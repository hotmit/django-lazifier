/*global jQuery, UI, gettext, document, Str */

window.DTbl = {
    locale: 'en',
    dateFormat: 'YYYY/MM/DD',
    dateTimeFormat: 'YYYY/MM/DD HH:mm',
    timeFormat: 'HH:mm',

    refreshDataTable: function(content, ajaxCommand){
        DTbl.initialize(ajaxCommand.options.localTarget);
    }
};

(function ($) {

    // region [ initializeJsDataTable ]
    DTbl.initializeJsDataTable = function(region) {
        if ($.fn.dataTable) {
            var pageLength = $.cookie('pageLength') || 10, opts, language = {
                emptyTable: gettext("No data available in table"),
                info: gettext("Showing _START_ to _END_ of _TOTAL_ entries"),
                infoEmpty: gettext("Showing 0 to 0 of 0 entries"),
                infoFiltered: gettext("(filtered from _MAX_ total entries)"),
                infoPostFix: "",
                thousands: gettext(","),
                lengthMenu: gettext("_MENU_"),
                loadingRecords: gettext("Loading..."),
                processing: gettext("Processing..."),
                search: gettext("Search:"),
                zeroRecords: gettext("No matching records found"),
                stateSave: true,
                paginate: {
                    first: gettext("First"),
                    last: gettext("Last"),
                    next: gettext("Next"),
                    previous: gettext("Previous")
                },
                aria: {
                    sortAscending: gettext(": activate to sort column ascending"),
                    sortDescending: gettext(": activate to sort column descending")
                }
            }, $region = $(region || document.body);

            opts = {
                lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, gettext('All')]],
                pageLength: Number(pageLength),
                language: language,
                dom: 'Blfrtp',
                buttons: [
                    'copyHtml5', 'csvHtml5', 'excelHtml5', 'pdfHtml5', 'print'
                ]
            };

            $region.find('.dt-table.paging').not('.no-data-table, :has(td[colspan])').DataTable(opts)
                .on('length.dt', function (e, settings, len) {
                    $.cookie('pageLength', len, {expires: 30, path: '/'});
                });

            $region.find('.dt-table').not('.paging, .no-data-table, :has(td[colspan])').DataTable({
                paging: false,
                language: language
            });
        }
    };
    // endregion

    // region [ initializeDateTimePicker ]
    DTbl.initializeDateTimePicker = function(region) {
        var $region = $(region),
            $picker = $region.find('.datetime-picker, .date-picker, .dateinput')
            .wrap('<div class="input-group date"></div>');

        $picker = $picker.parent();
        $picker.append('<span class="input-group-addon"><span class="glyphicon glyphicon-calendar"> </span></span>')
            .find('input')
            .addClass('form-control');

        // Initialize DateTime Picker
        $region.find('.datetime-picker').parent().datetimepicker({
            locale: DTbl.locale,
            format: DTbl.dateTimeFormat,
            showTodayButton: true
        }).on('dp.change', function (e) {
            //$(this).data('DateTimePicker').hide();
        });

        // Date Picker Only
        $region.find('.date-picker, .dateinput').parent().datetimepicker({
            locale: DTbl.locale,
            format: DTbl.dateFormat,
            showTodayButton: true
        }).on('dp.change', function (e) {
            $(this).data('DateTimePicker').hide();
        });

        // Time Picker Only
        $region.find('.time-picker').parent().datetimepicker({
            locale: DTbl.locale,
            format: DTbl.timeFormat,
            showTodayButton: false
        });
    };
    // endregion

    // region [ initializeMultiSelect ]
    DTbl.initializeMultiSelect = function(region, selector){
        selector = selector || '.selectmultiple';

        var $region = $(region || document.body), options = {
            enableClickableOptGroups: true,
            includeSelectAllOption: true,
            enableFiltering: true,
            maxHeight: 500,
            enableCaseInsensitiveFiltering: true,
            disableIfEmpty: true,
            selectAllText: gettext('Select All'),
            buttonText: function(options) {
                if (options.length == 0) {
                    return gettext('None Selected');
                }
                else if(options.length > 2){
                    return options.length + ' ' + gettext('items selected');
                }
                else{
                     var labels = [];
                     options.each(function() {
                         if ($(this).attr('label') !== undefined) {
                             labels.push($(this).attr('label'));
                         }
                         else {
                             labels.push($(this).html());
                         }
                     });
                     return labels.join(', ');
                }
            }
        };

        var $multiSelectElements = $region.find(selector);
        if ($.fn.multiSelect){
            $multiSelectElements = $multiSelectElements.not('.multi-select')
        }

        $multiSelectElements.multiselect(options).prop('required', false);
    };
    // endregion

    // region [ JQuery Multiselect Widget ]
    DTbl.initializeJqMultiselect = function(region, selector){
        if ($.fn.multiSelect){
            $(region).find(selector || '.multi-select').multiSelect({
                selectableOptgroup: true
            });
        }
    };
    // endregion

    // region [ Initialize any control in the specified region ]
    DTbl.initialize = function (region) {
        region = region || 'body';

        DTbl.initializeJsDataTable(region);
        DTbl.initializeDateTimePicker(region);
        DTbl.initializeMultiSelect(region);
        DTbl.initializeJqMultiselect(region);
    };
    // endregion

    // region [ Document Ready ]
    $(function () {
        var $body = $(document.body), $dtTable = $('.dt-list-view table'), dialogOptions = {}, uriSearch;

        function getDialogOption($src){
            var opts = {};
            $.each($src.data(), function(key, value){
                if (Str.startsWith(key, 'bsDialog')){
                    opts[Str.toCamelCase(key.replace('bsDialog', ''))] = value;
                }
            });
            return opts;
        }

        dialogOptions = getDialogOption($dtTable);
        uriSearch = new URI().search(true);

        $body.on('click', '.btn-dt-create', function(){
            var data = $.extend({}, uriSearch, $(this).data(), { mode: 'create' }), ajaxOptions = {
                    url: 'manage/',
                    method: 'GET',
                    data: data
                }, $dialog = UI.Patterns.bsDialogAjax(gettext('Create New'), ajaxOptions, dialogOptions, function(){
                    UI.Patterns.submitForm('form#frm-dt-create', '.dt-ajax-container', null, null, $dialog);
                });
        });

        $body.on('click', '.btn-dt-edit', function(){
            var data = $.extend({}, uriSearch, $(this).data(), { id: $(this).data('id'), mode: 'update' }), ajaxOptions = {
                    url: 'manage/',
                    method: 'GET',
                    data: data
                }, $dialog = UI.Patterns.bsDialogAjax(gettext('Update'), ajaxOptions, dialogOptions, function(){
                    UI.Patterns.submitForm('form#frm-dt-update', '.dt-ajax-container', null, null, $dialog);
                });
        });

        $body.on('click', '.btn-dt-delete', function(){
            var $btn = $(this), data = $.extend({}, uriSearch, $btn.data(), {
                id: $btn.data('id'),
                mode: 'delete',
                csrfmiddlewaretoken: $.cookie('csrftoken')
            });

            UI.Bs.confirmYesNo(gettext('Are you sure you want to delete this record?'),
                function(result){
                    if (result === true){
                        var ajaxOptions = {
                            url: 'manage/',
                            method: 'POST',
                            data: data
                        };

                        UI.Patterns.submitAjaxRequest(ajaxOptions);
                    }
                }
            );
        });

        $body.on('click', '.dt-action-btn.dt-modal-dialog', function(){
            var $btn = $(this),
                data = $.extend({}, uriSearch, $btn.data(), { mode: 'custom' }),
                btnDialogOption = getDialogOption($btn) || dialogOptions,
                ajaxOptions = {
                    url: $btn.data('url') || 'manage/',
                    method: 'GET',
                    data: data
                }, $dialog = UI.Patterns.bsDialogAjax(btnDialogOption.title || '', ajaxOptions, btnDialogOption,
                    function(){
                        UI.Patterns.submitForm('.dt-ajax-container form', '.dt-ajax-container',
                            null, null, $dialog);
                    });
        });

        $body.on('click', '.dt-action-btn.dt-action-command', function(){
            var $btn = $(this),
                data = $.extend({}, $btn.data(), { mode: 'custom', csrfmiddlewaretoken: $.cookie('csrftoken') }),
                ajaxOptions = {
                    url: $btn.data('url') || 'manage/',
                    method: 'POST',
                    data: data
                };

            function _submitRequest(){
                UI.Patterns.submitAjaxRequest(ajaxOptions, '.dt-list-view');
            }

            if (data.hasOwnProperty('confirm')){
                var confirmMsg = data.hasOwnProperty('confirmMsg') ? data.confirmMsg :
                    gettext('Are you sure you want to perform this action');

                delete data.confirm;
                delete data.confirmMsg;


                UI.Bs.confirmYesNo(confirmMsg,
                    function(result){
                        if (result === true){
                            _submitRequest();
                        }
                    }
                );
            }
            else {
                _submitRequest();
            }
        });

        DTbl.initialize();
    });
    // endregion

}(jQuery));
