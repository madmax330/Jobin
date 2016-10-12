
$(document).ready(function(){
	ChangeSelectState = function(){
		
        country_name= $('select[name=country]').val();
        request_url = 'get_states/' + country_name + '/';
        $.ajax({
            url: request_url,
            success: function(data){
				$('select[name=state]').empty();
                $.each(data, function(key, value){
                    $('select[name=state]').append('<option value="' + key + '">' + value +'</option>');
                });
            },
            
        })
    } 
	ChangeSelectState();
    $('select[name=country]').change(ChangeSelectState)
});