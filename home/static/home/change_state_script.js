
$(function(){

    ChangeSelectState = function(state){

        var country_name= $('select[name=country]').val();
        var request_url = 'get_states/' + country_name + '/';
        if(state)
            request_url += state + '/';

        $.ajax({
            url: request_url,
            success: function(data){
				$('select[name=state]').empty();
                $.each(data, function(key, value){
                    $('select[name=state]').append('<option value="' + value + '">' + value +'</option>');
                });
				if ($('select[name=country]').val() == "Canada")
				{
                   $("label[for='"+$('select[name=state]').attr('id')+"']").text('Province:');
                }
				else{
                    $("label[for='"+$('select[name=state]').attr('id')+"']").text('State:');
                }
            }

        })
    };


	if($(/^\s*update\s*$/.test($('.page-info-div').html()))) {
        ChangeSelectState($('#id_state').val());
    }
    else
        ChangeSelectState();

    $('select[name=country]').change(ChangeSelectState);

});
