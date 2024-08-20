src="https://js.stripe.com/v3/"

    let stripe = Stripe('{{ stripe_public_key }}');
    let elements = stripe.elements();
    let card = elements.create('card');
    card.mount('#card-element');

    card.on('change', function(event) {
        let displayError = document.getElementById('card-errors');
        if (event.error) {
            displayError.textContent = event.error.message;
        } else {
            displayError.textContent = '';
        }
    });

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