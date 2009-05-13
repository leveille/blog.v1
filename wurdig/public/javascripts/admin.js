WURDIG_ADMIN = {};
WURDIG_ADMIN.app = function()
{
    return {
        init: function()
        {
            /**
             * Delete confirmation
             */
            jQuery('a[href*="delete"]').bind('click', function(){
                return false;    
            });
        }
    };
}();

jQuery.noConflict();
jQuery(document).ready(function() {
    WURDIG_ADMIN.app.init();
});