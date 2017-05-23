
$(function(){

    let country_in = $('#id_country');
    let state_in = $('#id_state');

	if($(/^\s*update\s*$/.test($('.page-info-div').html())))
        get_state_data(country_in.val(), state_in.val());
    else
	    get_state_data(country_in.val(), 'none');


    country_in.change(function(){
        get_state_data(country_in.val(), 'none')
    });

});

function get_state_data(country, state){

    let request_url = '/home/get_states/' + country + '/' + state + '/';
    let state_in = $('#id_state');

    $.get(request_url, function(data, status){

        state_in.empty();
        $.each(data, function(key, value){
            state_in.append('<option value="' + value + '">' + value +'</option>');
        });
        if ($('select[name=country]').val() == "Canada")
            $("label[for=id_state]").text('Province:');
        else
            $("label[for=id_state]").text('State:');

    });
}





