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
                insert_markitup($(this));
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
            insert_markitup($(this));
        });
    });
}

/**
** MediaWidget binding with MarkItUp
*/

$(function(){
    $(".select_media").click(function(){
        insert_markitup($(this));
    });
}); 

/**
    select media from library & insert code
*/
var insert_markitup = function(file){
    file_url = file.val();
    media_type = $("#selectMediaType").val();
    file_pk = file.data("pk");
    file_desc = $("#mediaSelectDesc-"+file_pk).text()
    //
    var media_widget = parent.media_widget;
    media_widget.fb_helper.triggerInsert(file_url, media_type, file_desc);
    //the end
    media_widget.mediaWidget("close");
};

/**
    return to markItUp from upload & insert code
*/
function media_widget_markitup(file_url, media_type, description){
    var media_widget = parent.media_widget;
    media_widget.fb_helper.triggerInsert(file_url, media_type, description);
    media_widget.mediaWidget("close");
}
