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
            //Todo FEDE: Agregar una clase a los items que tienen submenues
            //para poder agregar flechas en el css :)
            //Acomodamos los sub-sub-menues en el dom, antes del span
            $(this).find('ul').find('ul').each(function(){
                //Lo alineamos a la izquierda
                var left = $(this).parent().width();
                $(this).css('left', left+'px');
                //Clonamos, lo insertamos al principio del li
                //y lo eliminamos
                var menu = $(this).clone();
                menu.prependTo($(this).parent());
                $(this).remove();
            });

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
                            hide();
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
                                        child_element.hide();
                                    }
                                );
                            }
                        });
                    }
                }
            });
        }
        //Por último, escondemos los menues
        $(this).find('ul').hide();
    });
});
