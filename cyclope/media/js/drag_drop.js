jQuery(function($) {
    $("#cyclope-relatedcontent-self_type-self_id-group, #question_set-group").sortable({
        //axis: 'y',
        placeholder: 'ui-state-highlight',
        forcePlaceholderSize: 'true',
        items: 'div.inline-related',
        update: updateInlineOrder
    });
    $("#cyclope-relatedcontent-self_type-self_id-group, #question_set-group").disableSelection();
});

function updateInlineOrder() {
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


jQuery(function($) {
    $("body.categorizations-changelist table#result_list").sortable({
        forcePlaceholderSize: 'true',
        items:'tr:gt(0)',
        update: updateChangelistOrder
    });
    $('body.categorizations-changelist input[id$=order]').css('display', 'none');
    $('body.categorizations-changelist input[id$=order]').after("<div class='order-arrow'>↕</div>");
    $("body.categorizations-changelist table#result_list").disableSelection();
});

function updateChangelistOrder(event, ui) {
    $('input[id$=order]').each(function (i, elem){
        $(elem).val(i+1);
    });
};
