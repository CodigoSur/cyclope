/**
    Multimedia Widget in Django - jQueryUI
    NumericA
-*/

$(function(){

    // bind select...
    $("#selectMediaType").change(function(){
        //...to hidden field
        $("#id_media_type").val($(this).val());
        //...to library list        /media_type
        $.get('/media_widget/library/'+$(this).val(), function(data){
            $("#select_media_widget").html(data);
            //re-bind
            $(".select_media").click(function(){
                insert_markitup($(this).val());
            });
        });
    });
    //retrieve value from hidden field
    if($("#id_media_type").val()){
        $("#selectMediaType").val($("#id_media_type").val());
    }

    // clean message alerts after 5s
    $(".message-row").delay(5000).fadeOut();

});

function n_per_page_change(n, val){
    url = '/media_widget/library/'+$("#id_media_type").val()+'?n='+n+'&nRows='+val;
    $.get(url, function(data){
        $("#select_media_widget").html(data);
        //re-bind
        $(".select_media").click(function(){
            insert_markitup($(this).val());
        });
    });
}

/**
    select media from library & insert code
*/
var insert_markitup = function(file_url){
    var media_widget = parent.media_widget;
    media_type = $("#selectMediaType").val();
    media_widget.fb_helper.triggerInsert(file_url, media_type);
    //the end
    media_widget.mediaWidget("close");
};

$(function(){
    $(".select_media").click(function(){
        insert_markitup($(this).val());
    });
}); 

/**
    return to markItUp from upload & insert code
*/
function media_widget_markitup(file_url, media_type){
    var media_widget = parent.media_widget;
    media_widget.fb_helper.triggerInsert(file_url, media_type);
    media_widget.mediaWidget("close");
}
