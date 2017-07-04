/**
 * Created by maxencecoulibaly on 5/14/17.
 */



function applicants_navigate(url) {
    let form = $('#filter-form');
    form.attr('action', url);
    form.submit();
}

$(function () {

    /*
     *   SINGLE APPLICANT VIEW FUNCTIONS
     */

    $('.request-cover').click(function () {
        send_get($(this).data('url'));
    });

    $('.discard-single-applicant').click(function () {
        let modal = $('#discard-modal');
        modal.find('.name').html($(this).data('name'));
        modal.find('.discard-accepted').attr('data-url', $(this).data('url'));
        modal.modal('show');
    });

    $('.discard-accepted').click(function () {
        $.get($(this).data('url'), function (data, status) {
            if (status === 'success') {
                applicants_navigate($('.single-next').data('url'));
            }
        })
            .fail(function (jqXHR) {
                $('#discard-modal').modal('hide');
                display_message(jqXHR.responseText, 'danger');
            });
    });

    /*
     *   SAVE APPLICATION FUNCTIONS
     */

    $('.save-btn').click(function () {
        send_get($(this).data('url'));
    });

    $('.remove-save').click(function () {
        send_get($(this).data('url'));
    });


    /*
     *   NAVIGATION
     */

    $('.to-single-view').click(function () {
        applicants_navigate($(this).data('url'));
    });

    $('.single-next').click(function () {
        applicants_navigate($(this).data('url'));
    });

    $('.single-prev').click(function () {
        applicants_navigate($(this).data('url'));
    });

    $('.to-multiple-view').click(function () {
        applicants_navigate($(this).data('url'));
    });

    /*
     *   FILTER RELATED FUNCTIONS
     */

    $('.clear-filter').click(function () {
        location.reload();
    });

    $('.search-in').keyup(function () {
        let results = $(this).siblings('.search-results');
        if ($(this).val()) {
            results.html('');
            hide(results);
            let search_val = $(this).val().toString().trim().toLowerCase();
            let pool = $('.jobin-schools');
            pool.children().each(function () {
                if ($(this).find('.search-result').html().toString().trim().toLowerCase().includes(search_val))
                    results.append($(this).html());
            });
            show(results);
        }
        else {
            hide(results);
        }

    });

    $(document.body).on('click', '.school-result', function () {
        show($('.filters-side-panel'));
        add_filter_value($(this).html().toString().trim(), 'school');
        let results = $('.search-results');
        hide(results);
        results.html('');
        results.siblings('.search-in').val('');
    });

    $('select#major-select').on('change', function () {
        let val = $(this).find('option:selected').val();
        if (val) {
            show($('.filters-side-panel'));
            add_filter_value(val, 'major');
        }
        $(this).val('');
    });

    $(document.body).on('click', '.remove-display-filter', function () {

        let parent = $(this).parents('.display-filter-value');
        hide(parent);

        if ($(this).hasClass('school')) {
            let input = $('#school_filter');
            let arr = remove_from_list(input.val().split(','), parent.find('.val').html().toString().trim());
            input.val(array_to_string(arr));
        }
        else if ($(this).hasClass('major')) {
            let input = $('#major_filter');
            let arr = remove_from_list(input.val().split(','), parent.find('.val').html().toString().trim());
            input.val(array_to_string(arr));
        }
        else {
            // error
            alert('error in class nomenclature.');
        }

    });

    $('#gpa_filter').keyup(function () {
        let gpa_error = $('.gpa-error');
        hide(gpa_error);
        let val = $(this).val();
        if(!val){
            hide($('.remove-gpa-filter'));
        }
        else if (val && isNaN(val)) {
            show(gpa_error);
        }
        else {
            show($('.filters-side-panel'));
            $('.display-gpa-filter').find('.gpa-filter-val').html($(this).val());
            show($('.gpa-filter-val'));
            show($('.remove-gpa-filter'));
        }
    });

    $('.remove-gpa-filter').click(function() {
        hide($('.gpa-filter-val'));
        $('#gpa_filter').val('');
        hide($(this));
    });

    $('input#filter_saved_true').on('change', function () {
        show($('.display-saved-filter'));
        show($('.filters-side-panel'));
    });

    $('input#filter_saved_false').on('change', function () {
        hide($('.display-saved-filter'));
    });

    $('.remove-saved-only').click(function () {
        $('#filter_saved_true').prop('checked', false);
        $('#filter_saved_false').prop('checked', true);
        hide($('.display-saved-filter'));
    });

});

function add_filter_value(val, list) {
    let container = $('.display-' + list + '-filter');
    let input = $('#' + list + '_filter');
    let str = input.val();
    if (str && $.inArray(val.toString(), str.split(',')) > -1)
        return;

    let html = `<div class="display-filter-value">
                    <span class="val">${val}</span>  
                    <span class="remove-display-filter right ${list} pointer">&times;</span>
                </div>`;

    container.append(html);

    if (str) {
        input.val(str + ',' + val);
    }
    else
        input.val(val);

}

function remove_from_list(arr, val) {
    let result = [];
    for (let i = 0; i < arr.length; i++) {
        if (arr[i] !== val)
            result.push(arr[i]);
    }
    return result;
}

function array_to_string(arr) {
    let result = '';
    if (arr.length > 0)
        result = arr[0].toString().trim();
    if (arr.length > 1) {
        for (let i = 1; i < arr.length; i++) {
            result += ',' + arr[i].toString().trim();
        }
    }
    return result;
}






