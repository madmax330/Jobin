
function validate_phone() {
    let phone_in = $('.phone-input');
    let phone = phone_in.val().toString().trim();
    let err = phone_in.siblings('.form-error');
    if (phone) {
        phone = phone.replace(/ /g, '').replace(/-/g, '').replace(/\(/g, '').replace(/\)/g, '');
        if (/^[0-9]{10}$/.test(phone))
            return true;
        else {
            err.addClass('alert alert-danger alert-dismissible');
            err.html('Phone number must have format ###-###-#### for example 800-800-8000');
            return false;
        }
    }
    else{
        return true;
    }
}