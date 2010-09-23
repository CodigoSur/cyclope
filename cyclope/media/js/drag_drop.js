jQuery(function($) {
    $("#cyclope-relatedcontent-self_type-self_id-group, #question_set-group").sortable({
        //axis: 'y',
        placeholder: 'ui-state-highlight',
        forcePlaceholderSize: 'true',
        items: 'div.inline-related',
        update: update
    });
    $("#cyclope-relatedcontent-self_type-self_id-group, #question_set-group").disableSelection();
});

function update() {
    $(this).find('div.inline-related').each(function(i) {
            $(this).find('input[id$=order]').val(i+1);
    });
};

jQuery(document).ready(function($){
    $(this).find('input[id$=order]').parent('div').parent('div').hide().parent().parent().css('cursor','move');
    $("#cyclope-relatedcontent-self_type-self_id-group .add-row a, #question_set-group .add-row a").click(function(){
        $("#cyclope-relatedcontent-self_type-self_id-group, #question_set-group").find('div.inline-related').each(function(i){
            $(this).find('input[id$=order]').val(i+1);
        })
    });
});

