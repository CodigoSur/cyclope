
function change_embed_widget(query_str){
    url = '/media_widget/library/'+$("#id_media_type").val()+query_str;
    $.get(url, function(data){
        $("#select_media_widget").html(data);
        //re-bind
        $(".select_media").click(function(){
            insert_markitup($(this).val());
        });
    });
}
