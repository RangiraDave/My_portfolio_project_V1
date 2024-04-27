$(document).ready(function() {
    $('form').submit(function(event) {
        event.preventDefault();  // Prevent the form from submitting
        $.ajax({
            url: "/check_email",  // Update this if your URL is different
            data: {'email': $('#email').val()},
            type: 'GET',
            success: function(response) {
                if (response.exists) {
                    $('#password-group').show();
                    $('#password').prop('required', true);  // Add the required attribute
                    $('form').unbind('submit');  // Unbind the event handler
                } else {
                    $('#email-message').html('<p class="error">This email does not exist in our system. Please signin if you do not have an account.</p>');
                }
            }
        });
    });
});