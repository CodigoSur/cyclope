$(function(){ 
    //VISOR
    visor = $("#media_widget_pictures", window.parent.document).clone();
    //mostrar en linea
    visor.find('img').each(function(){
        $(this).css('display', 'inline');
    });
    //solo fotos
    visor.find('input').remove();
    //cargar
    $("#visor_pictures_widget").html(visor.html());

    // clean message alerts after 8s
    $("#full-alert").delay(8000).fadeOut();

    window.setTimeout(keep_visor, 8000);
    $(".message-row").delay(8008).fadeOut();
});

function keep_visor(){ 
    flow = $("#full-alert").clone();
    flow.find(".message-row").remove();
    $(".container-fluid").prepend(flow.html());
}

function dance_hall_queen(tune, new_picture, remove_picture){
    var pictures_list = "" ;
    //pre-existent pictures
    inputs = $('[name="pictures"]', window.parent.document).map(function() { 
        return $(this).val(); 
    }).get();
    if(inputs!=""){
        pictures_list += inputs + ",";
    }
    //new picture
    if(tune == "blues"){
        pictures_list += new_picture += ",";
    }
    else if(tune == "reggae"){
        pictures_list = pictures_list.replace(remove_picture+",",'');
    }
    media_widget_refresh("pictures_list", pictures_list);
    delete_pictures_refresh(pictures_list);
    search_refresh(pictures_list);
}

//refresh parent (article's admin) widget pictures
function media_widget_refresh(type, param){
    url = type=="article_id" ? "/media_widget/pictures/widget/article/" : "/media_widget/pictures/widget/pictures/";
    url += param;
    $.get(url, function(data) {
        $("#media_widget", window.parent.document).html(data);
    });
}

function delete_pictures_refresh(pictures_list){
    url = "/media_widget/pictures/delete_list/"+pictures_list;
    $.get(url, function(data) {
        $("#delete").html(data);
    });
}

function search_refresh(pictures_list){ //param=LIB-pictures_list
    url = "/media_widget/pictures/widget/select/"+pictures_list;
    $.get(url, function(data) {
        $("#search").html(data);
    });
}

