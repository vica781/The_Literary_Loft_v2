from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
import stripe
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from .models import Order, OrderItem
from books.models import Book
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

def calculate_order_amount(request):
    cart = request.session.get('cart', {})
    total = 0
    for item in cart.values():
        total += item['price'] * item['quantity']
    return int(total * 100)  # Convert GBP to pence

def process_payment(request):
    currency = request.session.get('currency', 'gbp')  # Default to GBP
    amount = calculate_order_amount(request)
    
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount=amount,  # Amount in pence
            currency=currency,
            payment_method_types=["card"],
        )
        return render(request, 'payment.html', {'client_secret': intent.client_secret})
    except stripe.error.StripeError as e:
        # Handle error
        messages.error(request, "An error occurred during payment processing.")
        return redirect('checkout:checkout')  # to adjust redirect
    
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty")
        return redirect('books:book_list')

    total = calculate_order_amount(request)
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency=settings.STRIPE_CURRENCY,
    )

    context = {
        'client_secret': intent.client_secret,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'cart_items': cart,
        'total': total / 100,  # Convert back to pounds for display
    }
    return render(request, 'checkout/checkout.html', context)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WH_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_successful_payment_intent(payment_intent)
    # ... handle other event types

    return HttpResponse(status=200)

def handle_successful_payment_intent(payment_intent):
    # Logic to handle the successful payment
    # e.g., updating order status, sending a confirmation email, etc.
    pass

def order_success(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('books:book_list')

    total = calculate_order_amount(request) / 100  # Convert back to pounds
    order = Order.objects.create(
        user=request.user,
        order_number=str(uuid.uuid4()),
        total_amount=total,
    )

    for book_id, item in cart.items():
        book = Book.objects.get(id=book_id)
        OrderItem.objects.create(
            order=order,
            book=book,
            quantity=item['quantity'],
            price=item['price'],
        )

    # Clear the cart after successful order
    request.session['cart'] = {}

    return render(request, 'checkout/order_success.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'checkout/order_history.html', {'orders': orders})
