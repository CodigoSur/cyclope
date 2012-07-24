(function() {
    var hide_children = function (el){
        $(el).children('ul').stop(true, true).slideUp();
    }

    var show_children = function (el){
        $(el).children('ul').stop(true, true).slideDown();
    }

    var hide_all_expanded = function(){
        $(".cyclope_menu .expanded").each( function(){
            hide_children($(this));
            $(this).removeClass("expanded");
        })
    }

    $(document).ready(function(){
        // Hide children of collapsible menus not DISABLED
        $('.cyclope_menu:not(.disabled) .has_children').each(
            function(){$(this).next('ul').css('display', 'none');
        });


        $('html').click(function() {
            hide_all_expanded();
        });

        // select all menues that are not DISABLED
        $(".cyclope_menu:not(.disabled)").each(function(){
            if($(this).hasClass('on_click')){ // ON_CLICK
                $(this).find(".has_children").parent().click(function(event) {
                    event.stopPropagation();
                    if (!$(this).hasClass("expanded")){
                        hide_all_expanded();
                        show_children($(this));
                        $(this).addClass("expanded");
                        return false; // stop propagation to children
                    }
                });
            }else{
                // Expand children on mouse enter
                $(this).find("li").mouseenter(function() {
                    $(this).addClass("expanded");
                    show_children($(this));
                });

                // Collapse when leaving a menu item if the alignment is HORIZONTAL
                if ($(this).hasClass('horizontal')){
                    $(this).find("li").mouseleave(function() {
                        $(this).removeClass("expanded");
                        hide_children($(this));
                    });
                }
                // Collapse when leaving the whole menu if the alignment is VERTICAL
                else{
                    $(this).mouseleave(function(){
                        $(this).find("li").removeClass("expanded");
                        hide_children($(this).find('.has_children').parent());
                    });
                }
            }
        });
    });
})();
