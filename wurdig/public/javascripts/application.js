if(!this.WURDIG) {
    WURDIG = {};   
}
WURDIG.app = function(){
    return {
        init: function(){
            jQuery('#yui-main h2:first').addClass('wurdig-first');
            jQuery('div.required label').append(' <span class="error-message">*</span>');
            jQuery("div[id^='comment-'] h4").next('blockquote').addClass('bq-parent');
            jQuery('#wurdig-header-img h1, #wurdig-header-img h2, #wurdig-header-img h3, #wurdig-header-img p').fadeTo("slow", 0.5);
        }
    };
}();

jQuery.noConflict();
jQuery(document).ready(function(){
    WURDIG.app.init();
});
