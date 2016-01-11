$.widget("cyclope.mediaWidget", $.ui.dialog, {
    options: {
        autoOpen: false,
        modal: true,
        title: 'Subir archivos multimedia',
        minWidth: 400,
        minHeight: 400,
        closeText: "Cerrar"
    },
    position: function(objt){
        this.options.position = {my: "left top", at: "left button", of: objt}
    }
});
