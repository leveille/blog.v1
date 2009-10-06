if(!this.WURDIG) {
    WURDIG = {};   
}
WURDIG.app = function(){
    return {
        init: function(){
            jQuery('#yui-main h2:first').addClass('wurdig-first');
            jQuery('div.required label').append(' <span class="error-message">*</span>');
            jQuery("div[id^='comment-'] h4").next('blockquote').addClass('bq-parent');
			
			if (jQuery('body.about').length < 1) {
				//inject sidebar about me content from about page
				jQuery('#sidebar-about').load('/about #about-intro');
			}
        }
    };
}();

jQuery.noConflict();
jQuery(document).ready(function(){
    WURDIG.app.init();
    prettyPrint();
});
