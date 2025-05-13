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
let card = elements.create('card', {
	style: style
});
card.mount('#card-element');

// Handle real-time validation errors on the card element
card.addEventListener('change', function(event) {
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

// Handle form submit
let form = document.getElementById('payment-form');
form.addEventListener('submit', function(ev) {
	ev.preventDefault();
	console.log("Form submitted, starting payment process...");
	card.update({
		'disabled': true
	});
	$('#submit-button').attr('disabled', true);
	$('#payment-form').fadeToggle(100);
	$('#loading-overlay').fadeToggle(100);

	// Get the boolean value of the save_info checkbox
	let saveInfo = Boolean($('#id-save-info').prop('checked'));

	// From using the {% csrf_token %} in the form
	let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
	let postData = {
		'csrfmiddlewaretoken': csrfToken,
		'client_secret': stripe_client_secret,
		'save_info': saveInfo,
	};
	let url = '/checkout/cache_checkout_data/';

	$.post(url, postData).done(function() {
		console.log("Cache checkout data success, confirming card payment...");
		stripe.confirmCardPayment(stripe_client_secret, {
			payment_method: {
				card: card,
				billing_details: {
					name: $.trim(form.full_name.value),
					phone: $.trim(form.phone_number.value),
					email: $.trim(form.email.value),
					address: {
						line1: $.trim(form.street_address1.value),
						line2: $.trim(form.street_address2.value),
						city: $.trim(form.town_or_city.value),
						country: $.trim(form.country.value),
						postal_code: $.trim(form.postcode.value),
					}
				}
			}
		}).then(function(result) {
			if (result.error) {
				console.error("Payment failed:", result.error.message);
				let errorDiv = document.getElementById('card-errors');
				let html = `
                    <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
				$(errorDiv).html(html);
				$('#payment-form').fadeToggle(100);
				$('#loading-overlay').fadeToggle(100);
				card.update({
					'disabled': false
				});
				$('#submit-button').attr('disabled', false);
			} else {
				console.log("Payment successful, payment intent status:", result.paymentIntent.status);
				if (result.paymentIntent.status === 'succeeded') {
					form.submit();
				} else {
					console.error("Unexpected payment intent status:", result.paymentIntent.status);
				}
			}
		});
	}).fail(function(jqXHR, textStatus, errorThrown) {
		console.error("Cache checkout data failed:", textStatus, errorThrown);
		// Just reload the page, the error will be in django messages
		location.reload();
	});
});