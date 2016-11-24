
$(document).ready(function(){
	ChangeSelectState = function(){
		
        country_name= $('select[name=country]').val();
        request_url = 'get_states/' + country_name + '/';
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
            },
            
        })
    }
	
	ChangeSelectMajor = function(){
		
        program_name= $('select[name=program]').val();
        request_url = 'get_majors/' + program_name + '/';
        $.ajax({
            url: request_url,
            success: function(data){
				$('select[name=major]').empty();
                $.each(data, function(key, value){
                    $('select[name=major]').append('<option value="' + key + '">' + value +'</option>');
                });
				
            },
            
        })
    }

	ChangeSelectMajor();	
	ChangeSelectState();
	$('select[name=program]').change(ChangeSelectMajor)
    $('select[name=country]').change(ChangeSelectState)
});