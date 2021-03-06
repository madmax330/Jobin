/**
 * Created by maxencecoulibaly on 11/26/16.
 */

function validate_zipcode() {
    let country = $('.country-input').val();
    let zip_in = $('.zip-input');
    let err = zip_in.siblings('.form-error');
    country = country.toLowerCase();
    let z = zip_in.val().replace(" ", "").replace("-", "");
    if (z === "") {
        err.addClass('alert alert-danger alert-dismissible');
        err.html('Zip/postal code cannot be left empty.');
        scroll_to(zip_in);
        return false;
    }
    else {
        if (country === 'canada') {
            if (z.length > 6) {
                err.addClass('alert alert-danger alert-dismissible');
                err.html('Zip/postal Code value invalid. Example A1A 2A2');
                scroll_to(zip_in);
                return false;
            }
            if (/^[a-zA-Z][0-9][a-zA-Z][0-9][a-zA-Z][0-9]$/.test(z))
                return true;
            else {
                err.addClass('alert alert-danger alert-dismissible');
                err.html('Zip/postal Code value invalid. Example A1A 2A2');
                scroll_to(zip_in);
                return false;
            }
        }
        if (country === 'united states') {
            if (z.length > 5) {
                err.addClass('alert alert-danger alert-dismissible');
                err.html('Zip/postal code value invalid. Example 90210');
                scroll_to(zip_in);
                return false;
            }
            if (/^[0-9]{5}$/.test(z))
                return true;
            else {
                err.addClass('alert alert-danger alert-dismissible');
                err.html('Zip/postal code value invalid. Example 90210');
                scroll_to(zip_in);
                return false;
            }
        }
    }
}



