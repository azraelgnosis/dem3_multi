$(document).ready(function() {
    $('input#username').focusout(function() {
        let username = $(this).val();
        let taken = usernames.includes(username);
        if (taken) {
            $('#error-registration-username').html("Username is already taken");
        }
        else {
            $('#error-registration-username').html(null);
        }
    });
    
    $('input#password-check').focusout(function() {
        let password = $('input#password');
        console.log(password.val());
        let password_check = $(this);
        console.log(password_check.val());

        $('#error-registration-password').html(null);

        if (password.val() == password_check.val()) {
            password_check.css({'background-color': 'lightgreen'});
        } else {
            password_check.css({'background-color': 'brown'});
            $('#error-registration-password').html("Passwords don't match.")
        }
    });
});