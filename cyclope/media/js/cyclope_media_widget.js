/**
* TODO Move this & related scripts inside Cyclope's Media Widget App
*/

/** https://api.jquery.com/jquery.noconflict/ */

/**jQuery-UI Widget declaration*/
$.widget("cyclope.mediaWidget", $.ui.dialog, {
    options: {
        autoOpen: false,
        modal: true,
        title: 'Subir archivos multimedia',
        minWidth: 470,
        minHeight: 470,
        closeText: "Cerrar"
    },
    position: function(objt){
        this.options.position = {my: "left top", at: "right bottom", of: objt, collision: "fit"}
    }
});

/**Widget usage*/
$(function(){
    //form becomes widget
    $('#mediaUpload').mediaWidget();
    // picture button triggers widget
    $("#media_widget_button").click(function(){
        var widget = $("#mediaUpload").mediaWidget("position", this).mediaWidget("open");
    });
});
