let form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
    event.preventDefault();

    stripe.confirmCardPayment("{{ client_secret }}", {
        payment_method: {
            card: card,
        }
    }).then(function(result) {
        if (result.error) {
            // Show error to your customer
            let displayError = document.getElementById('card-errors');
            displayError.textContent = result.error.message;
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                // The payment has been processed!
                window.location.href = "{% url 'books:order_success' %}";
            }
        }
    });
});