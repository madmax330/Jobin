
$(function(){

    var program_in = $('#id_program');
    var major_in = $('#id_major');

	if($(/^\s*update\s*$/.test($('.page-info-div').html())))
        get_major_data(program_in.val(), major_in.val());
    else
        get_major_data(program_in.val(), 'none');

    program_in.change(function(){
        get_major_data(program_in.val(), 'none')
    });

});

function get_major_data(program, major){

    var request_url = '/home/get_majors/' + program + '/' + major + '/';
    var major_in = $('#id_major');

    $.get(request_url, function(data, status){

        major_in.empty();
        $.each(data, function(key, value){
            major_in.append('<option value="' + value + '">' + value +'</option>');
        });

    });
}





