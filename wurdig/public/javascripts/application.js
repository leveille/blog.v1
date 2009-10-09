if (!this.WURDIG) {
    WURDIG = {};
}
WURDIG.app = function(){
    return {
        init: function(){
            jQuery('#yui-main h2:first').addClass('wurdig-first');
            jQuery('div.required label').append(' <span class="error-message">*</span>');
            jQuery("div[id^='comment-'] h4").next('blockquote').addClass('bq-parent');
            
            /*if (jQuery('body.home').length > 0) {
                jQuery('#about-snippet').load('/about #about-intro', function(){
                    jQuery(this).slideDown('slow');
                });
            }*/
        }
    };
}();

jQuery.noConflict();
jQuery(document).ready(function(){
    WURDIG.app.init();
    prettyPrint();
});
