// RELATED CONTENTS

$(function() {
    $("#cyclope-relatedcontent-self_type-self_id-group, #question_set-group").sortable({
        //axis: 'y',
        placeholder: 'ui-state-highlight',
        forcePlaceholderSize: 'true',
        items: 'div.inline-related',
        update: updateInlineOrder
    });
    //TODO THIS IS THE CODE BLOCKING CONTENT TYPE SELECT!
    $("#cyclope-relatedcontent-self_type-self_id-group, #question_set-group").disableSelection();
});

function updateInlineOrder() {
    $(this).find('div.inline-related').each(function(i) {
        $(this).find('input[id$=order]').val(i+1);
    });
};

$(function(){
    $(this).find('input[id$=order]').parent('div').parent('div').hide().parent().parent().css('cursor','move');
    $("#cyclope-relatedcontent-self_type-self_id-group .add-row a, #question_set-group .add-row a").click(function(){
        $("#cyclope-relatedcontent-self_type-self_id-group, #question_set-group").find('div.inline-related').each(function(i){
            $(this).find('input[id$=order]').val(i+1);
        })
    });
});

// CATEGORIZATIONS

$(function(){
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

// DYNAMIC FORMS

$(function(){
    $("body.forms-form .inline-group .tabular.inline-related tbody").sortable({
        update: updateTableOrder,
        items: '> tr:has(input[id$=order][value!=""])', //limit sort to existing elements
    });
    //hide order and put an arrow
    $('body.forms-form input[id$=order]').css('display', 'none');
    $('body.forms-form input[id$=order]').after("<div class='order-arrow'>↕</div>");
});

function updateTableOrder(event, ui) {
    var y = 0; //start at 0, don't count empty fields
    $('input[id$=order]').each(function (i, elem){
        //form includes empty fields, only give an order to those fields having a label
        if($(elem).parent().parent().find("input[id$=label]").val() != ""){
            $(elem).val(y);
            y += 1;
        }
    });
};
