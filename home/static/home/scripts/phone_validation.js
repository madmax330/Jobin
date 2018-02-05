$(function() {
    $('form').submit(function () {

        let phone = $('.phone-input').val();
        let err = phone.siblings('.form-error');
        if(phone){
            phone = phone.replace(' ', '').replace('-', '');
            if(/^[0-9]{10}$/.test(phone))
                return true;
            else{
                err.addClass('alert alert-danger');
                err.html('Phone number must have format ###-###-#### for example 800-800-8000');
            }
        }

    });
});