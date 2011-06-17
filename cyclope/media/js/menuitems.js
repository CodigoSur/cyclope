$(document).ready(function(){

    $(".cyclope_menu").each(function(){
        var clickeable_items_collection = $(this).find('li').find('span.has_children a')
        if($(this).hasClass('on_click')){
        // todo Fede: Here we can add a script for sub-sub menus
            var item = null;
            clickeable_items_collection.toggle(
                function(ev){
                    ev.preventDefault();
                    item = $(this).parent().parent().children('ul');
                    item.slideDown();
                },
                function(ev){
                    ev.preventDefault();
                    item.slideUp();
                }
            );
        }else if($(this).hasClass('horizontal')){
            $(this).parent().find('ul').first()
            .children('li').each(function(){
                //Primero nos fijamos si tiene submenues
                if($(this).find('ul').length>0){
                    var parent_element = $(this).find('ul').first();
                    $(this).hover(
                        function(){
                            //Mostramos solo su primer submenues
                            parent_element.
                            stop(true,true).show(
                                'slide',
                                {direction: 'up'},
                                500
                            );
                        },
                        function(){
                            //Escondemos solo su primer submenues
                            parent_element.
                            hide(
                                'slide',
                                {direction: 'up'},
                                500
                            );
                        }
                    );
                    //Ahora nos fijamos si este submenu, tiene
                    //submenues
                    if(parent_element.find('ul').length>0){
                        //Tiene submenues, iteramos
                        //sobre sus hijos y confirmamos
                        //Cuales son aquellos que si tienen sub-sub-menues
                        parent_element.children('li').each(function(){
                            if($(this).find('ul').length>0){
                                //Tiene sub-sub-menues
                                var child_element = $(this).find('ul').first();
                                $(this).hover(
                                    function(){
                                        child_element.show('slide');
                                    },
                                    function(){
                                        child_element.hide('slide',
                                            {direction: 'left'}, 500
                                        );
                                    }
                                );
                            }                        
                        });
                    }
                }
            });
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        // todo Fede: Here we can refactor code so we can implement
        //              infinite sub-sub-menues            
        /*    $(this).children('li').each(function(){
                if($(this).children('ul').length > 0){
                    $(this).hover(
                        function(){
                            $(this).find('ul').first().stop(true, true).show('slide', {direction: 'up'});
                        },
                        function(){
                            $(this).find('ul').first()
                            .stop(true,true).hide('slide', {direction: 'up'});
                        }
                    );
                    if($(this).find('ul').find('ul').length > 0){
                        var element = $(this).find('ul').find('ul');
                        element.css('left', $(this).parent().width());
                        $(this).children('ul').children('li').each(function(){
                            if($(this).children('ul').length > 0){
                                var element = $(this).find('ul').first();
                                $(this).hover(
                                    function(){
                                        $(this).find('ul').first().stop(true, true).show('slide', {direction: 'up'});
                                    },
                                    function(){
                                    }
                                );                            
                        
        

                            }
                        });
                    }
                }
            });*/
            

        }
        //Acomodamos los sub-sub-menues
        $(this).find('ul').find('ul').each(function(){
            var left = $(this).parent().width();
            var top = $(this).parent().offset().top;
            //alert(top);
            $(this).css('left', left+'px');
            $(this).css('top', '0');
        });
        $(this).find('ul').hide();
        
    });
});
