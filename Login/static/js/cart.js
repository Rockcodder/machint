// cart.js

$(document).ready(function() {
    $('.add-to-cart-form').submit(function(e) {
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: '/add_to_cart',
            data: $(this).serialize(),
            success: function(response) {
                alert(response.message);
            },
            error: function(xhr) {
                alert(xhr.responseJSON.message);
            }
        });
    });
});
