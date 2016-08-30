/**
*** Insert the iframe from this script instead of including it as a template
**  allows us to display it only in forms using rich text fields, as markitup
*   is the default widget.
*/
function insert_media_iframe(){
    media_iframe = $('<iframe></iframe>');
    media_iframe.attr('src',"/media_widget/embed/new/picture"); //TODO(NumericA) {% url ... %}
    media_iframe.attr('width',"100%"); 
    media_iframe.attr('height',"100%");
    media_iframe.attr('frameborder',"0");
    media_iframe.css("min-height", "480px");
    //TODO(NumericA) AJAX media_iframe.html
    div_iframe = $('<div id="media_iframe"></div>');
    div_iframe.html(media_iframe);
    $('body').append(div_iframe);
}
$(function(){
    insert_media_iframe();
});

/**
*** jQuery-UI Widgets declaration
*/
/**Pictures Upload Widget*/
$.widget("cyclope.picturesWidget", $.ui.dialog, {
    options: {
        autoOpen: false,
        modal: true,
        title: gettext('Article images'),
        minWidth: 531,
        minHeight: 571,
        closeText: "Cerrar"
    },
    position: function(objt){
        this.options.position = {my: "left top", at: "right bottom", of: objt, collision: "fit"}
    }
});

var pictures_widget;

//bindings
$(function(){
    //form becomes widget
    $('#pictures_iframe').picturesWidget();
    // picture button triggers widget
    $("#media_widget").on('click', "#media_widget_button", function(){
        pictures_widget = $("#pictures_iframe").picturesWidget("position", this).picturesWidget("open");
    });
});

/**Embedded Media Widget*/
$.widget("cyclope.mediaWidget", $.ui.dialog, {
    options: {
        autoOpen: false,
        modal: true,
        title: gettext('Embed multimedia content'),
        minWidth: 470,
        minHeight: 480,
        closeText: gettext("Cerrar")
    },
    position: function(objt){
        this.options.position = {my: "left top", at: "right bottom", of: objt, collision: "fit"}
    },
    fb_helper: false
});
//bindings
$(function(){
    $('#media_iframe').mediaWidget();
});
// trigger is fired by markitup
