$(document).ready(function() {
    let register_username_valid = false;
    let register_password_valid = false;

    $('input#register-username').focusout(function() {
        let username = $(this).val().trim().toLowerCase();
        let taken = usernames.includes(username);
        let short = username.length <= 3;

        if (!short && !taken) {
            register_username_valid = true;
            $('#error-registration-username').html(null);
        } else {
            register_username_valid = false;

            if (taken) { $('#error-registration-username').html("Username is already taken."); }
            if (short) { $('#error-registration-username').html("Username must be at least 3 characters long."); }
        }
    });
    
    $('input#register-password-check, input#register-password').focusout(function() {
        let password = $('input#register-password');
        let password_check = $('input#register-password-check');
        let match = password.val().trim() == password_check.val().trim()
        let short = password.val().trim().length <= 3

        $('#error-registration-password').html(null);

        if (!short && match) {
            register_password_valid = true;
            password_check.css({'background-color': 'lightgreen'});
        } else {
            register_password_valid = false;
            password_check.css({'background-color': 'brown'});

            if (short) { $('#error-registration-password').html("Password must be at least 4 characters.\n"); }
            if (!match) { $('#error-registration-password').html("Passwords don't match.\n"); }
        }
    });

    $('input#register-username, #register-password, input#register-password-check').focusout(function() {
        if (register_username_valid && register_password_valid) {
            $('#register').prop('disabled', false);
        } else {
            $('#register').prop('disabled', true);
        }
    });


    let login_username_valid = false;
    let login_password_valid = false;

    $('input#login-username, input#login-password').focusout(function() {
        login_username_valid = ($('input#login-username').val().length > 0) ? true : false;
        login_password_valid = ($('input#login-password').val().length > 0) ? true : false;

        if (login_username_valid && login_password_valid) {
            $('input#login[type="submit"]').prop('disabled', false);
        } else {
            $('input#login[type="submit"]').prop('disabled', true);
        }
    });
});