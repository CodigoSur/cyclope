var query_str = '?n=';

function set_query_str(n){
    query_str += n;
    query_str += '&nRows=' + $(this).val();;
}

function append_query_str_smooth(url){
    return url+query_str;
}

function change_embed_widget(){
    url = '/media_widget/library/'+$("#id_media_type").val()+query_str;
    $.get(url, function(data){
        $("#select_media_widget").html(data);
        //re-bind
        $(".select_media").click(function(){
            insert_markitup($(this).val());
        });
    });
}
