if(!this.WURDIG) {
    WURDIG = {};   
}
WURDIG.admin = function()
{
    //private 
    return {
        cookie_prefix : 'wurdig.admin.',
        init: function()
        {
        
            /**
             * Delete confirmation
             */
            jQuery('a[href*="delete"]').bind('click', function(){
                return false;    
            });
        
            // Alternating Rows 
        	jQuery("table tbody tr:even").addClass("even");
        	jQuery("table tbody tr:odd").addClass("odd");
        
        	jQuery("#search input[type=text]").focus(function(){
               var field=jQuery("#search input[type=text]").val();
               if(field=="Enter key word(s)"){
                   jQuery("#search input[type=text]").val("");
               }
            });
        	jQuery("#search input[type=text]").blur(function(){
               var field=jQuery("#search input[type=text]").val();
               if(field==""){
                  jQuery("#search input[type=text]").val("Enter key word(s)");
               }
            });

            //finding if stored cookie for show/hide sidebar menu
            jQuery.each(jQuery('#secondary h3 a'), function(){
                if(WURDIG_UTILS.app.getCookie(WURDIG.admin.cookie_prefix + jQuery(this).text()) == "hide"){
                    jQuery(this).parent().next().addClass("hide");
                	jQuery(this).addClass("arrowLeft");
                	WURDIG_UTILS.app.setCookie(WURDIG.admin.cookie_prefix + jQuery(this).text(),"hide", 1000);
                }
            });
            
            //Show/Hide sidebar menu
            jQuery('#secondary h3 a').click(function () {
                if(this.className == "arrowLeft"){ //currently hiding
                    jQuery(this).parent().next().removeClass("hide");
                	jQuery(this).removeClass("arrowLeft");
                	WURDIG_UTILS.app.setCookie(WURDIG.admin.cookie_prefix + jQuery(this).text(),"show", 1000);
                }
                else{ //currently showing
                    jQuery(this).parent().next().addClass("hide");
                	jQuery(this).addClass("arrowLeft");
                	WURDIG_UTILS.app.setCookie(WURDIG.admin.cookie_prefix + jQuery(this).text(),"hide", 1000);
                }
                return false;
        	});// closing sidemenu click handler
        	
        	//checkbox master select all toggle
            jQuery('#primary thead th.form input:checkbox').click(function () {
                jQuery('#primary tbody td.form input:checkbox').each( function() {
                    this.checked = !this.checked;
                });	
            });
        	
        	
            if(!jQuery('#secondary h3.home').hasClass("active")){
                jQuery("#home-rounded-top").addClass("inactive");
            }

        	//background toggle for sidebar home menu
            jQuery('#secondary h3.home').hover(
                function () {
                    jQuery("#home-rounded-top").attr({class:''});
                    if(jQuery(this).hasClass("active")){
                        jQuery("#home-rounded-top").addClass("activehover");
                    }
                    else{//inactive - hover
                        jQuery("#home-rounded-top").addClass("inactivehover");
                    }
                },
                function () {
                    jQuery("#home-rounded-top").attr({class:''});
                    if(jQuery(this).hasClass("active")){
                        jQuery("#home-rounded-top").addClass("active");
                    }
                    else{
                        jQuery("#home-rounded-top").addClass("inactive");
                    }
                }
            );// closing sidemenu bg handler
        }
    };
    
}();

jQuery.noConflict();
jQuery(document).ready(function() {
    WURDIG.admin.init();
});