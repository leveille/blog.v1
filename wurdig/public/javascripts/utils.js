WURDIG_UTILS = {};
WURDIG_UTILS.app = function(){
    return {
        idPattern: /[0-9]+/,
        init: function(){
            jQuery('.js').show();
            WURDIG_UTILS.app.ajaxSetup();
            WURDIG_UTILS.app.message();
            WURDIG_UTILS.app.confirmDelete();
        },
        
        ajaxSetup: function(){
            jQuery("#loading").ajaxStart(function(){
                jQuery(this).show();
            }).ajaxStop(function(){
                jQuery(this).hide();
            });
        },
        
        /**
         * Provide a javascript dialog confirmation for delete actions
         */
        confirmDelete: function(){
            jQuery('a[href*="delete_confirm"]').bind('click', function(e){
                var sure = confirm("Are you positive you want to delete this item?");
                
                if (sure == true) {
                    var postUrl = jQuery(this)[0].pathname;
                    postUrl = postUrl.replace("delete_confirm", "delete");
                    var id = postUrl.match(WURDIG_UTILS.app.idPattern);
                    
                    jQuery.ajax({
                        type: "POST",
                        url: postUrl,
                        data: "id=" + id,
                        success: function(msg){
                            if (jQuery('.' + id).length > 0) {
                                jQuery('.' + id).animate({
                                    opacity: 0.6
                                }, 1000, function(){
                                    jQuery(this).fadeOut('slow', function(){
                                        WURDIG_UTILS.app.success('The item has successfully been deleted.');
                                    });
                                });
                            }
                            else {
                                var url = location.pathname;
                                //window.location = url.match(/\/[a-zA-Z0-9_-]+\/?/) + '?jsredirect&message=The+item+has+successfully+been+deleted.';
                            }
                        },
                        error: function(xhr, text){
                            WURDIG_UTILS.app.error('An unexpected error has occurred.');
                        }
                    });
                }
                e.preventDefault();
            });
        },
        
        message: function(){
            var url = location.search;
            var pattern = /message=/i;
            if (pattern.test(url)) {
                var parts = url.split(pattern);
                var message = parts[1];
                message = message.replace(/\+/g, " ");
                WURDIG_UTILS.app.success(message);
            }
        },
        
        success: function(message){
            jQuery('div.succ').html('<p class="message">' + message + '</p>').slideDown('slow', function(){
                setTimeout(function(){
                    jQuery('.message').slideUp('slow');
                }, 4000);
            });
        },
        
        error: function(message){
            jQuery('div.err').html('<p class="message">' + message + '</p>').slideDown('slow', function(){
                setTimeout(function(){
                    jQuery('.message').slideUp('slow');
                }, 4000);
            });
        }
    };
}();

jQuery.noConflict();
jQuery(document).ready(function(){
    WURDIG_UTILS.app.init();
});
