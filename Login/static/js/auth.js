// auth.js

$(document).ready(function() {
    $('#login-form').submit(function(e) {
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: '/authenticate',
            data: $(this).serialize(),
            success: function(response) {
                window.location.href = response.redirect;
            },
            error: function(xhr) {
                alert(xhr.responseJSON.message);
            }
        });
    });

    $('#signup-link').click(function(e) {
        e.preventDefault();
        // Implement signup logic here
        alert('Sign up functionality will be implemented soon!');
    });

    $('#forgot-password-link').click(function(e) {
        e.preventDefault();
        // Implement forgot password logic here
        alert('Forgot password functionality will be implemented soon!');
    });
});
