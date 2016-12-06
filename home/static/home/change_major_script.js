
$(function(){

    ChangeSelectMajor = function(major){

        var program_name= $('select[name=program]').val();
        var request_url = 'get_majors/' + program_name + '/';
        if(major)
            request_url += major + '/';
        $.ajax({
            url: request_url,
            success: function(data){
				$('select[name=major]').empty();
                $.each(data, function(key, value){
                    $('select[name=major]').append('<option value="' + value + '">' + value +'</option>');
                });

            }

        })
    };

    if($(/^\s*update\s*$/.test($('.page-info-div').html())))
        ChangeSelectMajor($('#id_major').val());
    else
        ChangeSelectMajor();

    $('select[name=program]').change(ChangeSelectMajor);

});
