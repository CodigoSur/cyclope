/**
* TODO Move this & related scripts inside Cyclope's Media Widget App
*/

/** https://api.jquery.com/jquery.noconflict/ */
var jQ2 = jQuery.noConflict(true);

/**jQuery-UI Widget declaration*/
jQ2.widget("cyclope.mediaWidget", jQ2.ui.dialog, {
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
jQ2(function(){
    //form becomes widget
    jQ2('#mediaUpload').mediaWidget();
    // picture button triggers widget
    jQ2("#media_widget_button").click(function(){
        var widget = jQ2("#mediaUpload").mediaWidget("position", this).mediaWidget("open");
    });
});
