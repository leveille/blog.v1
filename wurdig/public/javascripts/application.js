WURDIG = {};
WURDIG.app = function()
{
    return {
        init: function()
        {
            jQuery('#yui-main h2:first').addClass('wurdig-first');
        }
    };
}();

jQuery.noConflict();
jQuery(document).ready(function() {
    WURDIG.app.init();
});