/*global jQuery, DTbl */

(function (global, $) {
    "use strict";

    if (global.DTbl) {
        global.DTbl.initialize('.modal-content');
    }
}(typeof window !== 'undefined' ? window : this, jQuery));
