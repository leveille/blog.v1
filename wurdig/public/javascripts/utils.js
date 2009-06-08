if(!this.WURDIG_UTILS) {
    WURDIG_UTILS = {};   
}
WURDIG_UTILS.app = function(){
    return {
        idPattern: /[0-9]+/,
        init: function(){
            jQuery('.js').show();
            WURDIG_UTILS.app.ajaxSetup();
            WURDIG_UTILS.app.message();
            WURDIG_UTILS.app.confirm();
        },
        
        ajaxSetup: function(){
            jQuery("#loading").ajaxStart(function(){
                jQuery(this).show();
            }).ajaxStop(function(){
                jQuery(this).hide();
            });
        },
        
        /**
         * Provide a javascript dialog confirmation for actions
         */
        confirm: function(){
            jQuery('a[href*="_confirm"]').bind('click', function(e){
                var $that = jQuery(this);
                var sure = confirm("Are you positive you want to do that?");
                
                if (sure == true) {
                    var postUrl = jQuery(this)[0].pathname;
                    postUrl = postUrl.replace("_confirm", "");
                    var id = postUrl.match(WURDIG_UTILS.app.idPattern);
                    var isApprove = postUrl.indexOf("/approve") != -1;
                    var isDisapprove = postUrl.indexOf("/disapprove") != -1;
                    var isDelete = postUrl.indexOf("/delete") != -1;
                    jQuery.ajax({
                        type: "POST",
                        url: postUrl,
                        data: "id=" + id,
                        success: function(msg){
                            if (jQuery('.' + id).length > 0) {
                                //yes, yes, redundancy abounds.  bleh
                                if (isDelete) {
                                    jQuery('.' + id).animate({
                                        opacity: 0.6
                                    }, 1000, function(){
                                        jQuery(this).fadeOut('slow', function(){
                                            WURDIG_UTILS.app.success('The item has successfully been deleted.');
                                        });
                                    });
                                } else if (isApprove) {
                                    jQuery('.' + id).removeClass('action');
                                    var href = $that.attr('href');
                                    href = href.replace("approve_", "disapprove_");
                                    $that.text('Disapprove');
                                    $that.attr('href', href);
                                    WURDIG_UTILS.app.success('The item has successfully been approved.');
                                } else if (isDisapprove) {
                                    jQuery('.' + id).addClass('action');
                                    var href = $that.attr('href');
                                    href = href.replace("disapprove_", "approve_");
                                    $that.attr('href', href);
                                    $that.text('Approve');
                                    WURDIG_UTILS.app.success('The item has successfully been disapproved.');
                                }
                            }
                            else {
                                var url = location.pathname;
                                window.location = url.match(/\/[a-zA-Z0-9_-]+\/?/) + '?jsredirect&message=Your+request+has+been+completed+successfully.';
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
