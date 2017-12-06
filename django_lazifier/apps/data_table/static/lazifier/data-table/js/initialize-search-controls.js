/*global jQuery, DTbl */

(function (global, $) {
    "use strict";

    $(function(){
        if (global.DTbl) {
            global.DTbl.initializeDateTimePicker('form.dt-filter-form');
            global.DTbl.initializeMultiSelect('form.dt-filter-form');
        }
    });
}(typeof window !== 'undefined' ? window : this, jQuery));
