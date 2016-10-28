
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
				if ($('select[name=country]').val() == "Canada")
				{					
                   $("label[for='"+$('select[name=state]').attr('id')+"']").text('Province:');
                }
				else{					
                    $("label[for='"+$('select[name=state]').attr('id')+"']").text('State:');
                }
            },
            
        })
    } 
	ChangeSelectState();
    $('select[name=country]').change(ChangeSelectState)
});