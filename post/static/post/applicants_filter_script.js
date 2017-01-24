/**
 * Created by maxencecoulibaly on 1/23/17.
 */


$(function(){

    var school_in = $('#school-input');
    var major_in = $('#major-input');
    var gpa_in = $('#id_gpa_filter');

    var school_filters = school_in.val().toString().split(',');
    var major_filters = major_in.val().toString().split(',');
    var gpa_filter = parseInt(gpa_in.val());

    if(gpa_filter == 0)
        gpa_in.val('');

    $('.school-val').each(function(){
        var t = $(this);
        for(var i=0; i<school_filters.length; i++){
            if(t.val() == school_filters[i])
                t.prop('checked', true);
        }
    });

    $('.major-val').each(function(){
        var t = $(this);
        for(var i=0; i<major_filters.length; i++){
            if(t.val() == major_filters[i])
                t.prop('checked', true);
        }
    });

});









