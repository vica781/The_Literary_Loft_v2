const stripePublicKey = document.getElementById('id_stripe_public_key').textContent.slice(1, -1);
const clientSecret = document.getElementById('id_client_secret').textContent.slice(1, -1);

const stripe = Stripe(stripePublicKey);
const elements = stripe.elements();
const card = elements.create('card', {style: {base: {color: '#000'}}});
card.mount('#card-element');

// Handle real-time validation errors
card.addEventListener('change', function(event) {
    const errorDiv = document.getElementById('card-errors');
    if (event.error) {
        errorDiv.textContent = event.error.message;
    } else {
        errorDiv.textContent = '';
    }
});

const paymentForm = document.getElementById('payment-form');

if (paymentForm) {
    paymentForm.addEventListener('submit', function(ev) {
        ev.preventDefault();
        // Disable the card element and submit button to prevent multiple submissions
        card.update({ 'disabled': true });
        document.getElementById('submit-button').disabled = true;

        // Get form data
        const form = document.getElementById('payment-form');
        const fullName = form.querySelector('#id_full_name').value;
        const email = form.querySelector('#id_email').value;

        // Handle save info checkbox
        const saveInfo = Boolean(document.getElementById('id-save-info')?.checked);
        const setDefaultInfo = Boolean(document.getElementById('id-set-default-info')?.checked);

        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const postData = {
            'csrfmiddlewaretoken': csrfToken,
            'client_secret': clientSecret,
            'save_info': saveInfo,
            'set_default_info': setDefaultInfo
        };

        const url = '/checkout/cache_checkout_data/';

        // First cache the checkout data
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams(postData),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not OK.');
            }
            
            // Then confirm the card payment with Stripe
            return stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        name: fullName,
                        email: email,
                    }
                }
            });
        })
        .then(function(result) {
            if (result.error) {
                // Show error to customer
                const errorDiv = document.getElementById('card-errors');
                errorDiv.textContent = result.error.message;
                
                // Re-enable the form elements
                card.update({ 'disabled': false });
                document.getElementById('submit-button').disabled = false;
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    // Payment succeeded, submit the form
                    form.submit();
                }
            }
        })
        .catch(function(error) {
            // Better error handling
            console.error('Error:', error);
            const errorDiv = document.getElementById('card-errors');
            errorDiv.textContent = 'There was a problem processing your payment. Please try again.';
            
            // Re-enable the form elements
            card.update({ 'disabled': false });
            document.getElementById('submit-button').disabled = false;
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

    const resetButton = document.querySelector('button[type="reset"]');
    if (resetButton) {
        resetButton.addEventListener('click', function() {
            card.clear();
            const cardErrors = document.getElementById('card-errors');
            if (cardErrors) {
                cardErrors.textContent = '';
            }
        });
    }
});