/**
* TODO Move this & related scripts inside Cyclope's Media Widget App
*/

/** https://api.jquery.com/jquery.noconflict/ */

/**jQuery-UI Widgets declaration*/

/**Pictures Upload Widget*/

$.widget("cyclope.picturesWidget", $.ui.dialog, {
    options: {
        autoOpen: false,
        modal: true,
        title: 'Imágenes del Artículo',
        minWidth: 470,
        minHeight: 470,
        closeText: "Cerrar"
    },
    position: function(objt){
        this.options.position = {my: "left top", at: "right bottom", of: objt, collision: "fit"}
    }
});
//bindings
$(function(){
    //form becomes widget
    $('#pictures_iframe').picturesWidget();
    // picture button triggers widget
    $("#media_widget_button").click(function(){
        var widget = $("#pictures_iframe").picturesWidget("position", this).picturesWidget("open");
    });
});

/**Embedded Media Widget*/
$.widget("cyclope.mediaWidget", $.ui.dialog, {
    options: {
        autoOpen: false,
        modal: true,
        title: 'Insertar Contenido Multimedia',
        minWidth: 470,
        minHeight: 470,
        closeText: "Cerrar"
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


