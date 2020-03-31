$(document).ready(function() {
    let username_valid = false;
    let password_valid = false;

    $('input#username').focusout(function() {
        let username = $(this).val().toLowerCase();
        let taken = usernames.includes(username);
        if (taken) {
            username_valid = false;
            $('#error-registration-username').html("Username is already taken");
        }
        else {
            username_valid = true;
            $('#error-registration-username').html(null);
        }
    });
    
    $('input#password-check, #password').focusout(function() {
        let password = $('input#password');
        let password_check = $('input#password-check');

        $('#error-registration-password').html(null);

        if (password.val() == password_check.val()) {
            password_valid = true;
            password_check.css({'background-color': 'lightgreen'});
        } else {
            password_valid = false;
            password_check.css({'background-color': 'brown'});
            $('#error-registration-password').html("Passwords don't match.")
        }
    });

    $('input#username, #password, input#password-check').focusout(function() {
        if (username_valid && password_valid) {
            $('#register').prop('disabled', false);
        } else {
            $('#register').prop('disabled', true);
        }
    });
});