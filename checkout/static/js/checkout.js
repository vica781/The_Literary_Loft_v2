let paymentForm = document.getElementById('payment-form');

if (paymentForm) {
    paymentForm.addEventListener('submit', function(event) {
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
}

document.addEventListener('DOMContentLoaded', function() {
    const guestCheckoutBtn = document.getElementById('guest-checkout-btn');
    const checkoutFormContainer = document.getElementById('checkout-form-container');

    if (guestCheckoutBtn) {
        guestCheckoutBtn.addEventListener('click', function() {
            checkoutFormContainer.style.display = 'block';
            guestCheckoutBtn.parentElement.parentElement.style.display = 'none';
        });
    }
});
