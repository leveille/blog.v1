WURDIG = {};
WURDIG.app = function()
{
    return {
        styleguide_fetched : false,
        init: function()
        {
            jQuery('#yui-main h2:first').addClass('wurdig-first');
            jQuery('#comment-styleguide').bind('click', function(){
                var $guide_container = jQuery(this).parent().find('div');
                if(!WURDIG.app.styleguide_fetched) {
                    $guide_container.load("/comment-styleguide div.entry", function(){
                        WURDIG.app.styleguide_fetched = true;    
                    });
                }
                $guide_container.toggleClass('hide');
                return false;  
            });
            jQuery('div.required label').append(' <span class="error-message">*</span>');
            jQuery("div[id^='comment-'] h4").next('blockquote').addClass('bq-parent');
            jQuery("a[rel='external'], a._blank").bind('click', function(){
                window.open(this.href);
                return false;
            });
        }
    };
}();

jQuery.noConflict();
jQuery(document).ready(function() {
    WURDIG.app.init();
});