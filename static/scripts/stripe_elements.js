// this is the same file as in the CI videos

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe('pk_test_51K8jexEE3VLVHzWc8ckIVJpmSWAhlhOnT7nz8ioOry3z0atx9lyoXk3K2njUw23ZsTs21nofTig1QnoY31ni4H0s00njCJPUBc');
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
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
var card = elements.create('card', {
    style: style
});
card.mount('#payment-element');

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
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
var form = document.getElementById('payment-form');

form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    card.update({
        'disabled': true
    });
    $('#pay-now-button').attr('disabled', true);
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function (result) {
        if (result.error) {
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            card.update({
                'disabled': false
            });
            $('#pay-now-button').attr('disabled', false);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});

// duplicates the above functionality to post the form to the database
// when submit is triggered, by clicking the pay-now-button, submitFormData() is called
form.addEventListener('submit', function (e) {
    e.preventDefault()
    console.log('Form Submitted...', total);
    submitFormData()
})


function submitFormData() {
    console.log('Payment button clicked')

    // gets user data
    var userFormData = {
        'name': form.name.value,
        'email': form.email.value,
        'total': total,
    }

    // gets user shipping address from the form
    var shippingInfo = {
        'address': form.address.value,
        'street': form.street.value,
        'city': form.city.value,
        'county': form.county.value,
        'postcode': form.postcode.value,
    }


    console.log('Shipping Info:', shippingInfo)
    console.log('User Info:', userFormData)
    alert('User Info:')
   

    var url = "process_order/"
		fetch(url, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': csrftoken,
				},
				body: JSON.stringify({
					'form': userFormData,
					'shipping': shippingInfo
				}),

			})
			.then((response) => response.json())
			.then((data) => {
				console.log('Success:', data);
				alert('Transaction completed');
				// below resets the cookie
				cart = {}
				document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
				// below sends the user to a designated page, e.g. home
				window.location.href = "{% url 'home' %}"

			})
}