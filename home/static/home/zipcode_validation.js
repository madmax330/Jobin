/**
 * Created by maxencecoulibaly on 11/26/16.
 */

$(function(){

    $('form').submit(function(){
        var country = $('#id_country').val();
        var zip_in = $('#id_zipcode');
        var err = zip_in.parents('.form-element').first().find('.form-error');
        country = country.toLowerCase();
        var z = zip_in.val().replace(" ", "");
        if(z == ""){
            err.addClass('danger-message alert');
            err.addClass('message');
            err.html('Zip code cannot be left empty.');
            return false;
        }
        if(country == 'canada'){
            if(z.length > 6){
                err.addClass('danger-message alert');
                err.addClass('message');
                err.html('Zip Code value invalid. Example A1A 2A2');
                return false;
            }
            if(/^[a-zA-Z][0-9][a-zA-Z][0-9][a-zA-Z][0-9]$/.test(z))
                return true;
            else{
                err.addClass('danger-message alert');
                err.addClass('message');
                err.html('Zip Code value invalid. Example A1A 2A2');
                return false;
            }
        }
        if(country == 'united states'){
            if(z.length > 5){
                err.addClass('danger-message alert');
                err.addClass('message');
                err.html('Zip code value invalid. Example 90210');
                return false;
            }
            if(/^[0-9]{5}$/.test(z))
                return true;
            else{
                err.addClass('danger-message alert');
                err.addClass('message');
                err.html('Zip code value invalid. Example 90210');
                return false;
            }
        }
    });
});



