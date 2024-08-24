/*
Core logic/payment flow for this comes from here:
https://stripe.com/docs/payments/accept-a-payment

CSS from here:
https://stripe.com/docs/stripe-js
*/

// Get the stripe public key and client secret from the template
let stripe_stripe_public_key = document.getElementById('id_stripe_public_key').textContent.slice(1, -1);
let stripe_client_secret = document.getElementById('id_client_secret').textContent.slice(1, -1);
let stripe = Stripe(stripe_stripe_public_key);
let elements = stripe.elements();

// Set up Stripe.js and Elements to use in checkout form
let style = {
    base: {
        color: '#000',
        fontFamily: '"Roboto", sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

// Create an instance of the card Element
let card = elements.create('card', {style: style});
card.mount('#card-element');

// Handle real-time validation errors on the card element
card.addEventListener('change', function (event) {
    let errorDiv = document.getElementById('card-errors');
    if (event.error) {
        let html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});
