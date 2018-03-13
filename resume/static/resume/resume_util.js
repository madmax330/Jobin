/**
 * Created by maxencecoulibaly on 5/7/17.
 */

let WALKTHROUGH = false;


function send_walkthrough(url, form, info) {
    form.find('.fa-spinner').removeClass('w3-hide');
    $.post(url, form.serialize(), function (data, status) {

        if (status === 'success') {
            form.find('.fa-spinner').addClass('w3-hide');
            $('.modal-messages').html('');
            if (info['caller'] === 'resume') {
                if(data === 'resume complete')
                    location.reload();
                clear_form('resume-form');
                close_modal('resume-modal');
                $('#school-form').attr('action', '/resume/new/school/' + data + '/');
                $('#language-form').attr('action', '/resume/new/language/' + data + '/');
                $('#experience-form').attr('action', '/resume/new/experience/' + data + '/');
                $('#award-form').attr('action', '/resume/new/award/' + data + '/');
                $('#skill-form').attr('action', '/resume/new/skill/' + data + '/');
                $('#reference-form').attr('action', '/resume/new/reference/' + data + '/');
                open_modal('school-modal');
                display_modal_message('New resume created successfully.', 'success');
            }
            else if (info['caller'] === 'school') {
                clear_form('school-form');
                display_modal_message('School successfully added to resume.', 'success');
                if (info['action'] === 'continue') {
                    close_modal('school-modal');
                    open_modal('language-modal');
                }
                else if (info['action'] === 'another') {
                    show_next_walk_button('school-modal');
                }
            }
            else if (info['caller'] === 'language') {
                clear_form('language-form');
                display_modal_message('Language successfully added to resume.', 'success');
                if (info['action'] === 'continue') {
                    close_modal('language-modal');
                    open_modal('experience-modal');
                }
                else if (info['action'] === 'another') {
                    show_next_walk_button('language-modal');
                }
            }
            else if (info['caller'] === 'experience') {
                clear_form('experience-form');
                display_modal_message('Experience successfully added to resume.', 'success');
                if (info['action'] === 'continue') {
                    close_modal('experience-modal');
                    open_modal('award-modal');
                }
                else if (info['action'] === 'another') {
                    show_next_walk_button('experience-modal');
                }
            }
            else if (info['caller'] === 'award') {
                clear_form('award-form');
                display_modal_message('Award successfully added to resume.', 'success');
                if (info['action'] === 'continue') {
                    close_modal('award-modal');
                    open_modal('skill-modal');
                }
                else if (info['action'] === 'another') {
                    show_next_walk_button('award-modal');
                }
            }
            else if (info['caller'] === 'skill') {
                clear_form('skill-form');
                display_modal_message('Skill successfully added to resume.', 'success');
                if (info['action'] === 'continue') {
                    close_modal('skill-modal');
                    open_modal('reference-modal');
                }
                else if (info['action'] === 'another') {
                    show_next_walk_button('skill-modal');
                }
            }
            else if (info['caller'] === 'reference') {
                clear_form('reference-form');
                display_modal_message('Reference successfully added to resume.', 'success');
                if (info['action'] === 'continue') {
                    close_modal('reference-modal');
                    location.reload()
                }
                else if (info['action'] === 'another') {
                    show_next_walk_button('reference-modal');
                }
            }
        }

    })
        .fail(function (jqXHR) {
            display_modal_message(jqXHR.responseText, 'danger');
        });
}

$(function () {

    if ($('.first-resume').html() === 'true') {
        WALKTHROUGH = true;
        MODAL_BLOCK = true;
        open_modal('resume-modal');
        $('.walk-buttons').each(function () {
            show($(this));
        });
        $('.regular-buttons').each(function () {
            hide($(this));
        });
        $('.first-message').each(function () {
            show($(this));
        });
        $('#school_program').val($('.student-program').html().toString().trim());
        $('#school_level').val('university');
    }

    $('.complete-resume').click(function(){
        let parent = $(this).parents('.jobin-resume');
        WALKTHROUGH = true;
        MODAL_BLOCK = true;
        $('.walk-buttons').each(function () {
            show($(this));
        });
        $('.regular-buttons').each(function () {
            hide($(this));
        });
        $('.first-message').each(function () {
            show($(this));
        });
        $('#school_name').val($('.student-school').html().toString().trim());
        $('#school_program').val($('.student-program').html().toString().trim());
        $('#school_level').val('university');
        $('#school-form').attr('action', parent.find('.school-url').html().toString().trim());
        $('#language-form').attr('action', parent.find('.language-url').html().toString().trim());
        $('#experience-form').attr('action', parent.find('.experience-url').html().toString().trim());
        $('#award-form').attr('action', parent.find('.award-url').html().toString().trim());
        $('#skill-form').attr('action', parent.find('.skill-url').html().toString().trim());
        $('#reference-form').attr('action', parent.find('.reference-url').html().toString().trim());
        open_modal('school-modal');
    });

    $('.activate-resume').click(function() {
        send_get($(this).data('url'));
    });

    /* RESUME FUNCTIONS */

    $('.new-resume').click(function () {
        show($('.other-resumes'));
        $('#resume-form').attr('action', $(this).data('url'));
        clear_form('resume-form');
        open_modal('resume-modal');
    });

    $('.edit-resume').click(function () {
        let parent = $(this).parents('.jobin-resume');

        let name = parent.find('.name').html().toString().trim();
        let gpa = parent.find('.gpa').html();

        $('#resume_name').val(name);
        if (gpa)
            $('#resume_gpa').val(gpa.toString().trim());

        $('#resume-form').attr('action', $(this).data('url'));
        hide($('.other-resumes'));
        open_modal('resume-modal');
    });

    $('#resume-form').submit(function (event) {
        event.preventDefault();

        if (WALKTHROUGH){
            send_walkthrough($(this).attr('action'), $(this), {caller: 'resume'});
        }
        else {
            submit_resume_info($(this).attr('action'), $(this));
        }

    });

    /* LANGUAGE FUNCTIONS */

    $('.new-language').click(function () {
        clear_form('language-form');
        open_modal('language-modal');
    });

    $('.language-next').click(function () {
        clear_form('language-form');
        close_modal('language-modal');
        open_modal('experience-modal');
    });

    $('.language-save-continue').click(function () {

        let form = $('#language-form');
        send_walkthrough(form.attr('action') + '?api=true', form, {caller: 'language', action: 'continue'});

    });

    $('.language-save-another').click(function () {

        let form = $('#language-form');
        send_walkthrough(form.attr('action') + '?api=true', form, {caller: 'language', action: 'another'});

    });

    $('.edit-language').click(function ( event ) {
        event.preventDefault();
        let parent = $(this).parents('.jobin-language');

        let name = parent.find('.name').html().toString().trim();
        let level = parent.find('.level').html().toString().trim();

        $('#language_name').val(name);
        $('#language_level').val(level.toLowerCase());

        $('#language-form').attr('action', $(this).data('url'));

        open_modal('language-modal');

    });

    $('#language-form').submit(function (event) {
        event.preventDefault();

        submit_resume_info($(this).attr('action'), $(this));

    });

    /* SCHOOL FUNCTIONS */

    $('.new-school').click(function () {
        clear_form('school-form');
        open_modal('school-modal');
    });

    $('.school-next').click(function () {
        clear_form('school-form');
        close_modal('school-modal');
        open_modal('language-modal');
    });

    $('.school-save-continue').click(function () {

        let form = $('#school-form');
        send_walkthrough(form.attr('action') + '?api=true', form, {caller: 'school', action: 'continue'});

    });

    $('.school-save-another').click(function () {

        let form = $('#school-form');
        send_walkthrough(form.attr('action') + '?api=true', form, {caller: 'school', action: 'another'});

    });

    $('.edit-school').click(function ( event ) {
        event.preventDefault();
        let parent = $(this).parents('.jobin-school');

        let name = parent.find('.name').html().toString().trim();
        let start = parent.find('.start').html().toString().trim();
        let end = parent.find('.end').html().toString().trim();
        let level = parent.find('.level').html().toString().trim();
        let program = parent.find('.program').html();

        $('#school_name').val(name);
        $('#school_start').val(get_input_date(start));
        $('#school_level').val(level.toLowerCase());

        if (program)
            $('#school_program').val(program.toString().trim());

        let e = $('#school_end');
        if (end.toLowerCase() === 'current school') {
            e.val('');
            e.prop('disabled', true);
            $('#school_current').prop('checked', true);
        }
        else {
            e.prop('disabled', false);
            e.val(get_input_date(end));
            $('#school_current').prop('checked', false);
        }

        $('#school-form').attr('action', $(this).data('url'));

        open_modal('school-modal');

    });

    $('#school-form').submit(function (event) {
        event.preventDefault();

        submit_resume_info($(this).attr('action'), $(this));

    });

    $('#school_current').on('change', function() {
        let s = $('#school_end');
        if($(this).prop('checked')){
            s.val('');
            s.prop('disabled', true);
        }
        else{
            s.prop('disabled', false);
        }
    });

    /* EXPERIENCE FUNCTIONS */

    $('.new-experience').click(function () {
        clear_form('experience-form');
        open_modal('experience-modal');
    });

    $('.experience-next').click(function () {
        clear_form('experience-form');
        close_modal('experience-modal');
        open_modal('award-modal');
    });

    $('.experience-save-continue').click(function () {

        let form = $('#experience-form');
        send_walkthrough(form.attr('action') + '?api=true', form, {caller: 'experience', action: 'continue'});

    });

    $('.experience-save-another').click(function () {

        let form = $('#experience-form');
        send_walkthrough(form.attr('action') + '?api=true', form, {caller: 'experience', action: 'another'});

    });

    $('.edit-experience').click(function ( event ) {
        event.preventDefault();
        let parent = $(this).parents('.jobin-experience');

        let title = parent.find('.title').html().toString().trim();
        let start = parent.find('.start').html().toString().trim();
        let end = parent.find('.end').html().toString().trim();
        let type = parent.find('.type').html().toString().trim();
        let company = parent.find('.company').html().toString().trim();
        let description = parent.find('.description').html();

        $('#experience_title').val(title);
        $('#experience_start').val(get_input_date(start));
        $('#experience_company').val(company);
        $('#experience_type').val(type.toLowerCase());

        if (description)
            $('#experience_description').val(description.toString().trim().replace('<br/>', '\n'));

        let e = $('#experience_end');
        if (end.toLowerCase() === 'current job') {
            e.val('');
            e.prop('disabled',true);
            $('#experience_current').prop('checked', true);
        }
        else {
            e.prop('disabled', false);
            e.val(get_input_date(end));
            $('#experience_current').prop('checked', false);
        }

        $('#experience-form').attr('action', $(this).data('url'));

        open_modal('experience-modal');

    });

    $('#experience-form').submit(function (event) {
        event.preventDefault();

        submit_resume_info($(this).attr('action'), $(this));

    });

    $('#experience_current').on('change', function() {
        let e = $('#experience_end');
        if($(this).prop('checked')){
            e.val('');
            e.prop('disabled', true);
        }
        else{
            e.prop('disabled', false);
        }
    });

    /* AWARD FUNCTIONS */

    $('.new-award').click(function () {
        clear_form('award-form');
        open_modal('award-modal');
    });

    $('.award-next').click(function () {
        clear_form('award-form');
        close_modal('award-modal');
        open_modal('skill-modal');
    });

    $('.award-save-continue').click(function () {

        let form = $('#award-form');
        send_walkthrough(form.attr('action') + '?api=true', form, {caller: 'award', action: 'continue'});

    });

    $('.award-save-another').click(function () {

        let form = $('#award-form');
        send_walkthrough(form.attr('action') + '?api=true', form, {caller: 'award', action: 'another'});

    });

    $('.edit-award').click(function ( event ) {
        event.preventDefault();
        let parent = $(this).parents('.jobin-award');

        let title = parent.find('.title').html().toString().trim();
        let date = parent.find('.date').html().toString().trim();
        let type = parent.find('.type').html().toString().trim();
        let description = parent.find('.description').html().toString().trim();

        $('#award_title').val(title);
        $('#award_date').val(get_input_date(date));
        $('#award_type').val(type.toLowerCase());
        $('#award_description').val(description.replace('<br/>', '\n'));

        $('#award-form').attr('action', $(this).data('url'));

        open_modal('award-modal');

    });

    $('#award-form').submit(function (event) {
        event.preventDefault();

        submit_resume_info($(this).attr('action'), $(this));

    });

    /* SKILL FUNCTIONS */

    $('.new-skill').click(function () {
        clear_form('skill-form');
        open_modal('skill-modal');
    });

    $('.skill-next').click(function () {
        clear_form('skill-form');
        close_modal('skill-modal');
        open_modal('reference-modal');
    });

    $('.skill-save-continue').click(function () {

        let form = $('#skill-form');
        send_walkthrough(form.attr('action') + '?api=true', form, {caller: 'skill', action: 'continue'});

    });

    $('.skill-save-another').click(function () {

        let form = $('#skill-form');
        send_walkthrough(form.attr('action') + '?api=true', form, {caller: 'skill', action: 'another'});

    });

    $('.edit-skill').click(function ( event ) {
        event.preventDefault();
        let parent = $(this).parents('.jobin-skill');

        let name = parent.find('.name').html().toString().trim();
        let level = parent.find('.level').html().toString().trim();
        let description = parent.find('.description').html();

        $('#skill_name').val(name);
        $('#skill_level').val(level.toLowerCase());
        if (description)
            $('#skill_description').val(description.toString().trim());

        $('#skill-form').attr('action', $(this).data('url'));

        open_modal('skill-modal');

    });

    $('#skill-form').submit(function (event) {
        event.preventDefault();

        submit_resume_info($(this).attr('action'), $(this));

    });

    /* REFERENCES FUNCTIONS */

    $('.new-reference').click(function() {
        clear_form('reference-form');
        open_modal('reference-modal');
    });

    $('.reference-next').click(function () {
        clear_form('reference-form');
        close_modal('reference-modal');
        location.reload();
    });

    $('.reference-save-continue').click(function () {

        WALKTHROUGH = false;
        let form = $('#reference-form');
        send_walkthrough(form.attr('action') + '?api=true', form, {caller: 'reference', action: 'continue'});

    });

    $('.reference-save-another').click(function () {

        let form = $('#reference-form');
        send_walkthrough(form.attr('action') + '?api=true', form, {caller: 'reference', action: 'another'});

    });

    $('.edit-reference').click(function( event ) {
        event.preventDefault();
        let parent = $(this).parents('.jobin-reference');

        let name = parent.find('.name').html().toString().trim();
        let affiliation = parent.find('.affiliation').html().toString().trim();
        let email = parent.find('.email').html().toString().trim();

        $('#reference_name').val(name);
        $('#reference_affiliation').val(affiliation);
        $('#reference_email').val(email);

        $('#reference-form').attr('action', $(this).data('url'));

        open_modal('reference-modal');

    });

    $('#reference-form').submit(function (event) {
        event.preventDefault();

        submit_resume_info($(this).attr('action'), $(this));

    });

});

function submit_resume_info(url, form) {
    form.find('.fa-spinner').removeClass('w3-hide');
    $.post(url, form.serialize(), function(data, status){

        if(status === 'success'){
            form.find('.fa-spinner').addClass('w3-hide');
            location.reload();
        }

    })
        .fail(function(jqXHR){
            form.find('.fa-spinner').addClass('w3-hide');
            display_modal_message(jqXHR.responseText, 'danger');
        });
}

function show_next_walk_button(val) {
    let btn = $('#' + val).find('.next-btn');
    if (btn.hasClass('w3-hide'))
        btn.removeClass('w3-hide');
}
