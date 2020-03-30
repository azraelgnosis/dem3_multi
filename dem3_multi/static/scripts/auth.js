$(document).ready(function() {
    $('input#password-check').on('input', function() {
        let password = $('input#password');
        console.log(password.val());
        let password_check = $(this);
        console.log(password_check.val());

        if (password.val() == password_check.val()) {
            password_check.css({'background-color': 'lightgreen'});
        } else {
            password_check.css({'background-color': 'brown'});
        }
    });
});