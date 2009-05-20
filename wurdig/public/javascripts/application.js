WURDIG = {};
WURDIG.app = function(){
    function fetch_styleguide($container)
    {
        if (!WURDIG.app.styleguide_fetched) {
            $container.load("/comment-styleguide div.wurdig-entry", function(){
                WURDIG.app.styleguide_fetched = true;
            });
        }
    }
    function styleguide () 
    {
        $guide_href = jQuery('#comment-styleguide');
        var $guide_container = $guide_href.parent().find('div');
        fetch_styleguide($guide_container);
        
        $guide_href.bind('click', function() {
            $guide_container.slideToggle('slow');
            return false;
        });
    }
    return {
        styleguide_fetched: false,
        init: function(){
            styleguide();
            jQuery('#yui-main h2:first').addClass('wurdig-first');
            jQuery('div.required label').append(' <span class="error-message">*</span>');
            jQuery("div[id^='comment-'] h4").next('blockquote').addClass('bq-parent');
            jQuery('#wurdig-header-img h1, \
                #wurdig-header-img h2, \
                #wurdig-header-img h3, \
                #wurdig-header-img p').fadeTo("slow", 0.5);
        }
    };
}();

jQuery.noConflict();
jQuery(document).ready(function(){
    WURDIG.app.init();
});
