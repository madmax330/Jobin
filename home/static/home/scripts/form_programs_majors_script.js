/**
 * Created by maxencecoulibaly on 5/21/17.
 */



$(function() {
    let program = $('.program-input').val();
    update_programs(program);
    let majors = $('.major-input');
    if (majors.length)
        update_majors(program, majors.val());

    $('select.program-input').on('change', function(){
        let new_value = $(this).find('option:selected').val();
        if(majors.length) {
            majors.html('');
            update_majors(new_value, '');
        }
    });

});

function update_programs(program){
    let program_in = $('.program-input');

    $('.jobin-program').each(function(){
        let val = $(this).html().toString().trim();
        if(val !== program)
            program_in.append(`<option value="${val}">${val}</option>`);
    });
}

function update_majors(program, major){
    let major_in = $('.major-input');

    $('.jobin-major').each(function(){
        let val = $(this).html().toString().trim();
        if($(this).data('program') === program && val !== major)
            major_in.append(`<option value="${val}">${val}</option>`);
    });
}

