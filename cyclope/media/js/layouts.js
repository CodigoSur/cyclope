jQuery(document).ready(function($){

    //APPEARANCE
    $("#regionview_set-group h2").after($("#regions_tree"))
    $("#regions_tree").show();

    /**
    *** CHAINED SELECTS
    */
    // chained select for layout's regionviews
    $("select[id^='id_regionview_set-'][id$='-region']").each(function(i, sel){
        setup_chainedSelect_for_layout(i, true);
    });
    // new regionview chained select
    $("#regionview_set-group .add-row a").click(function() {
        setup_chainedSelect_for_layout($("select[id^='id_regionview_set-'][id$='-region']").length - 2, false);
    });  
    $('#id_template').trigger('change');

    /**
    *** VIEW OPTIONS
    */    
    $.cyclope = {access_number: [], initial_content: []};
    $("select[id^='id_regionview_set-'][id$='-content_view']").each(function(i, sel){
        $.cyclope.access_number[i] = 2;
        var prefix = "#id_regionview_set-" + i + "-"
        var div_container = $("#regionview_set-"+i+"-view_options_multiple").parent().parent();
        var html = $("#regionview_set-" + i + "-view_options_multiple").html() || "";
        if (html && (html.indexOf("form-row") !== -1)){
            $.cyclope.initial_content[i] = true;
        }
        else {
            div_container.hide();
            $.cyclope.initial_content[i] = false;
        }
        $(this).change(function(){
            update_to_default_view_options($(this), prefix, div_container, i);
        });
    });
    
    /**
    *** SINGLE REGIONVIEW EDITION
    */
    //hide all fieldsets
    regionviews_hide_all();
    //for all region view links
    $('.edit_region_view').each(function(){
        //on click select their region fieldset
        $(this).click(function(){
            regionview_id = $(this).attr('data-regionview');
            regionviews_hide_all();
            regionview = $("input[id^='id_regionview_set-'][id$='-id'][value="+regionview_id+"]").parent()
            regionview.show();
            jump_bottom();
        });
    });
    //for add to region + img links
    $('.add_view_to_region').each(function(){
        $(this).click(function(){
            regionviews_hide_all();
            region = $(this).attr('data-region');
            //$("#regionview_set-empty").show();
            last_region_id = $("select[id^='id_regionview_set-'][id$='-region']").length - 2
            setup_chainedSelect_for_layout(last_region_id, false);
            $('select[id="id_regionview_set-'+last_region_id+'-region"]').val(region);
            $('#regionview_set-'+last_region_id).show();
            jump_bottom();
        });
    });
    
// END $
});

/**
*** HELPERS
*/

//CHAINED SELECT
function setup_chainedSelect_for_layout(i, notTriggetParentChange) {

    $("#id_regionview_set-" + i + "-region").chainedSelect({
        parent: '#id_template',
        accesor_function: function (param){ return layout_data["layout_templates"][param]; },
        value: 'region_name',
        label: 'verbose_name',
        notTriggetParentChange: notTriggetParentChange,
    });

    $("#id_regionview_set-" + i + "-content_view").chainedSelect({
        parent: '#id_regionview_set-' + i + '-content_type',
        accesor_function: function (param){ return layout_data["views_for_models"][param]; },
        value: 'view_name',
        label: 'verbose_name',
        notTriggetParentChange: notTriggetParentChange,
    });

    $("#id_regionview_set-" + i + "-object_id").chainedSelect({
        parent: '#id_regionview_set-' + i + '-content_type',
        url: '/'+cyclope_prefix+'objects_for_ctype_json',
        value: 'object_id',
        label: 'verbose_name',
        notTriggetParentChange: notTriggetParentChange,
    });

    if ($('#id_regionview_set-' + i + '-content_type').val()){
        $('#id_regionview_set-' + i + '-content_type').trigger('change');
    }
}

// SINGLE REGIONVIEW EDITION
function regionviews_hide_all(){
    $('.dynamic-regionview_set').hide();
}
function jump_bottom(){
    $("html, body").animate({ scrollTop: $(document).height() }, "slow");
}

// VIEW OPTIONS
function update_to_default_view_options(view_options_combo, prefix, div_container, i){
    var view_name = view_options_combo.val();
    var content_type_id = $(prefix+"content_type  option:selected").val()
    
    if (view_name && content_type_id){
        $.get("/"+cyclope_prefix+"options_view_widget_html", {
                content_type_id: content_type_id,
                view_name: view_name,
                prefix_name: "regionview_set-"+i+"-"
            }, 
            function(data){
                if (data){
                    $("#regionview_set-" + i + "-view_options_multiple").replaceWith(data);
                    div_container.show();
                }
                else{
                    $("#regionview_set-" + i + "-view_options_multiple").html("");
                    div_container.hide();
                }
            }
        );
    }
    else {
        $("#regionview_set-" + i + "-view_options_multiple").html("");
        div_container.hide();
    }
}
