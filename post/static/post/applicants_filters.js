
let FILTERS = {
    schools: [],
    majors: [],
    gpa: '',
    saved: false
};

let SCHOOLS = [];
let SCHOOL_SEARCH_RESULTS = [];

$(function(){

    load_schools();
    load_filters();
    render_filters();

    $('.clear-filter').click(function () {
        location.reload();
    });

    $('select#major-select').on('change', function () {
        let val = $(this).find('option:selected').val();
        if (val) {
            if (FILTERS.majors.indexOf(val)) {
                FILTERS.majors.push(val);
                update_filter_input_values();
                render_filters();
            }
        }
        $(this).val('');

    });

    $(document.body).on('click', '.remove-filter-item', function() {
        if ($(this).hasClass('school-filter-value')) {
            remove_filter_value('school', $(this).siblings().text().toString().trim());
        }
        else if($(this).hasClass('major-filter-value')) {
            remove_filter_value('major', $(this).siblings().text().toString().trim());
        }
        update_filter_input_values();
        render_filters();
    });

    $('#gpa_filter').keyup(function () {
        let gpa_error = $('.gpa-error');
        hide(gpa_error);
        let val = $(this).val();
        if (val && isNaN(val)) {
            show(gpa_error);
        }
        else if(Number(val) > 4) {
            show(gpa_error);
        }
        else {
            FILTERS.gpa = val;
            render_filters();
        }
    });

    $('.school-search-in').keyup(function () {
        SCHOOL_SEARCH_RESULTS = [];
        let results = $('.school-search-results');
        if ($(this).val()) {
            hide(results);
            let search_val = $(this).val().toString().trim().toLowerCase();
            for(let i=0; i<SCHOOLS.length; i++){
                if (SCHOOLS[i].toLowerCase().includes(search_val))
                    SCHOOL_SEARCH_RESULTS.push(SCHOOLS[i]);
            }
            render_school_search_results();
        }
        else {
            hide(results);
        }
    });

    $(document.body).on('click', '.school-result', function () {
        let school = $(this).text().toString().trim();
        if (FILTERS.schools.indexOf(school))
            FILTERS.schools.push(school);
        hide($('.school-search-results'));
        $('.school-search-in').val('');
        update_filter_input_values();
        render_filters();
    });

    $('input#filter_saved_true').on('change', function () {
        FILTERS.saved = $(this).prop('checked');
        render_filters();
    });

    $('input#filter_saved_false').on('change', function () {
        FILTERS.saved = !$(this).prop('checked');
        render_filters();
    });

    $('input#filter_keep_false').change(function() {
        if($(this).is(':checked')){
            show($('.delete-non-filtered'));
        }
        else{
            hide($('.delete-non-filtered'));
        }
    });

    $('input#filter_keep_true').change(function() {
        if($(this).is(':checked')){
            hide($('.delete-non-filtered'));
        }
        else{
            show($('.delete-non-filtered'));
        }
    });

});

function load_schools() {

    $('.jobin-schools').children().each(function () {
        SCHOOLS.push($(this).text().toString().trim());
    });

}


function load_filters() {

    let schools = $('#school_filter').val();
    let majors = $('#major_filter').val();
    let gpa = $('#gpa_filter').val();
    let saved = $('#filter_saved_true').prop('checked');

    if (schools)
        FILTERS.schools = schools.split(',');
    if (majors)
        FILTERS.majors = majors.split(',');
    if (gpa)
        FILTERS.gpa = gpa;
    FILTERS.saved = saved;

}

function render_filters() {

    let school_container = $('.school-filters-container');
    let major_container = $('.major-filters-container');

    if (FILTERS.schools.length > 0) {
        school_container.html('<ul>');
        for (let i=0; i<FILTERS.schools.length; i++) {
            school_container.append(get_display_filter_string('school-filter-value', FILTERS.schools[i]));
        }
        school_container.append('</ul>');
    }
    else {
        school_container.html('<span>No Filters</span>')
    }


    if (FILTERS.majors.length > 0) {
        major_container.html('<ul>');
        for (let i=0; i<FILTERS.majors.length; i++) {
            major_container.append(get_display_filter_string('major-filter-value', FILTERS.majors[i]));
        }
        major_container.append('</ul>');
    }
    else {
        major_container.html('<span>No Filters</span>')
    }

    if (FILTERS.gpa)
        $('.gpa-filter-val').text(FILTERS.gpa);
    else
        $('.gpa-filter-val').text('None');

    $('.only-saved-val').text(FILTERS.saved ? 'True' : 'False');

}

function remove_filter_value(filter_type, filter_value) {
    if (filter_type === 'school') {
        let i = FILTERS.schools.indexOf(filter_value);
        if (i >= 0)
            FILTERS.schools.splice(i, 1);
    }
    else if(filter_type === 'major') {
        let i = FILTERS.majors.indexOf(filter_value);
        if (i >= 0)
            FILTERS.majors.splice(i, 1);
    }
}

function update_filter_input_values() {

    $('#school_filter').val(array_to_string(FILTERS.schools));
    $('#major_filter').val(array_to_string(FILTERS.majors));

}

function get_display_filter_string(filter_type, filter_value) {

    return `<li><span class="val">${filter_value}</span> <span class="remove-filter-item ${filter_type}">&times;</span></li>`;

}

function render_school_search_results(){
    let results = $('.school-search-results');
    results.html('');
    for (let i=0; i<SCHOOL_SEARCH_RESULTS.length; i++){
        results.append(get_school_search_result_string(SCHOOL_SEARCH_RESULTS[i]));
    }
    show(results);
}

function get_school_search_result_string(val) {

    return `<div class='search-result school-result'>${val}</div>`;

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












