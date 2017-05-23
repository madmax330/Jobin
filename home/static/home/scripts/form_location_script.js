/**
 * Created by maxencecoulibaly on 5/21/17.
 */


$(function(){
    let country = $('.country-input');
    let state = $('.state-input');
    update_countries(country.val());
    update_states(country.val(), state.val());

    $('select.country-input').on('change', function(){
        let new_value = $(this).find('option:selected').val();
        state.html('');
        update_states(new_value, '');
    });
});

function update_countries(country){
    let country_in = $('.country-input');
    $('.jobin-country').each(function(){
        let val = $(this).html().toString().trim();
        if(val !== country)
            country_in.append(`<option value="${val}">${val}</option>`);
    });
}

function update_states(country, state){
    let state_in = $('.state-input');

    if(country === 'Canada') {
        state_in.siblings('label').html('Province:');
        $('.zip-label').html('Postal Code:');
    }
    else {
        state_in.siblings('label').html('State:');
        $('.zip-label').html('Zipcode:');
    }


    $('.jobin-state').each(function(){
        let val = $(this).html().toString().trim();
        if($(this).data('country') === country && val !== state)
            state_in.append(`<option value="${val}">${val}</option>`);
    });
}


