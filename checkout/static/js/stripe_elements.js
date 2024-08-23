let stripe_stripe_public_key = document.getElementById('id_stripe_public_key').textContent.slice(1, -1);
let stripe_client_secret = document.getElementById('id_client_secret').textContent.slice(1, -1);
let stripe = Stripe(stripe_stripe_public_key);
let elements = stripe.elements();


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

let card = elements.create('card', {style: style});
card.mount('#card-element');