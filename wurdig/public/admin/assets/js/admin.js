if(!this.WURDIG.admin) {
    WURDIG.admin = {};   
}
WURDIG.admin.app = function()
{
    //private 
    return {
        init: function()
        {
        
            /**
             * Delete confirmation
             */
            jQuery('a[href*="delete"]').bind('click', function(){
                return false;    
            });
        
            jQuery('table.form sup').tooltip();
        
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
            $.each(jQuery('#secondary h3 a'), function(){
                if(WURDIG_ADMIN.utils.getCookie(jQuery(this).text()) == "hide"){
                    jQuery(this).parent().next().addClass("hide");
                	jQuery(this).addClass("arrowLeft");
                	WURDIG_ADMIN.utils.setCookie(jQuery(this).text(),"hide", 1000);
                }
            });
            
            //Show/Hide sidebar menu
            jQuery('#secondary h3 a').click(function () {
                if(this.className == "arrowLeft"){ //currently hiding
                    jQuery(this).parent().next().removeClass("hide");
                	jQuery(this).removeClass("arrowLeft");
                	WURDIG_ADMIN.utils.setCookie(jQuery(this).text(),"show", 1000);
                }
                else{ //currently showing
                    jQuery(this).parent().next().addClass("hide");
                	jQuery(this).addClass("arrowLeft");
                	WURDIG_ADMIN.utils.setCookie(jQuery(this).text(),"hide", 1000);
                }
                return false;
        	});// closing sidemenu click handler
        	
        	//checkbox master select all toggle
            jQuery('#primary thead th.form input:checkbox').click(function () {
                jQuery('#primary tbody td.form input:checkbox').each( function() {
                    this.checked = !this.checked;
                });
                     	
            });// closing sidemenu click handler
        	
        	
            if(!jQuery('#secondary h3.home').hasClass("active")){
                jQuery("#home-rounded-top").addClass("inactive");
            }

        	//background toggle for sidebar home menu
            jQuery('#secondary h3.home').hover(
                function () {
                    jQuery("#home-rounded-top").attr({class:''});
                    if(jQuery(this).hasClass("active")){
                        console.log("home active hover");
                        jQuery("#home-rounded-top").addClass("activehover");
                    }
                    else{//inactive - hover
                        console.log("home inactive hover");
                        jQuery("#home-rounded-top").addClass("inactivehover");
                    }
                },
                function () {
                    jQuery("#home-rounded-top").attr({class:''});
                    if(jQuery(this).hasClass("active")){
                        console.log("home active unhover");
                        jQuery("#home-rounded-top").addClass("active");
                    }
                    else{
                        console.log("home inactive unhover");
                        jQuery("#home-rounded-top").addClass("inactive");
                    }
                }
            );// closing sidemenu bg handler
        }
    };
    
})();

jQuery.noConflict();
jQuery(document).ready(function() {
    WURDIG.admin.app.init();
});