$(document).ready(function() {
    let username_valid = false;
    let password_valid = false;

    $('input#username').focusout(function() {
        let username = $(this).val().trim().toLowerCase();
        let taken = usernames.includes(username);
        let short = username.length <= 3;

        if (!short && !taken) {
            username_valid = true;
            $('#error-registration-username').html(null);
        } else {
            username_valid = false;

            if (taken) { $('#error-registration-username').html("Username is already taken."); }
            if (short) { $('#error-registration-username').html("Username must be at least 3 characters long."); }
        }
    });
    
    $('input#password-check, input#password').focusout(function() {
        let password = $('input#password');
        let password_check = $('input#password-check');
        let match = password.val().trim() == password_check.val().trim()
        let short = password.val().trim().length <= 3

        $('#error-registration-password').html(null);

        if (!short && match) {
            password_valid = true;
            password_check.css({'background-color': 'lightgreen'});
        } else {
            password_valid = false;
            password_check.css({'background-color': 'brown'});

            if (short) { $('#error-registration-password').html("Password must be at least 4 characters.\n"); }
            if (!match) { $('#error-registration-password').html("Passwords don't match.\n"); }
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