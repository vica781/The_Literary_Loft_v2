from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import stripe
import uuid

from .models import Order, OrderItem
from books.models import Book
from .forms import OrderForm


# Helper Functions

def calculate_order_amount(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return int(total * 100)  # Convert GBP to pence


def handle_successful_payment_intent(payment_intent):
    # Logic to handle successful payment
    pass


# Main Views
def checkout(request):  # checkout view
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There is nothing in your bag at the moment. Please, add items to your bag before checking out.")
        return redirect('books:book_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            total = calculate_order_amount(request) / 100  # Convert back to pounds
            order.total_amount = total
            order.order_number = str(uuid.uuid4())
            order.save()

            for book_id, item in cart.items():
                book = Book.objects.get(id=int(book_id))
                OrderItem.objects.create(
                    order=order,
                    book=book,
                    quantity=item['quantity'],
                    price=item['price']
                )
            request.session['cart'] = {}
            messages.success(request, "Order placed successfully.")
            
            return redirect('books:order_success')
    else:
        form = OrderForm()

    # Calculate total and create PaymentIntent
    total = calculate_order_amount(request)
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount=total,
            currency=settings.STRIPE_CURRENCY,
        )
    except stripe.error.StripeError as e:
        messages.error(request, "An error occurred while creating the payment intent.")
        return redirect('checkout:checkout')

    # Prepare cart items for display
    cart_items = []
    total_display = 0
    for book_id, item in cart.items():
        book = Book.objects.get(id=int(book_id))
        item_total = item['quantity'] * float(item['price'])
        total_display += item_total
        cart_items.append({
            'book': book,
            'quantity': item['quantity'],
            'price': item['price'],
            'total': item_total
        })

    context = {
        'order_form': form,
        'cart_items': cart_items,
        'total': total_display,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WH_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)  # Invalid payload
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)  # Invalid signature

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_successful_payment_intent(payment_intent)

    return HttpResponse(status=200)


@login_required
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

    # Clear the cart after a successful order
    request.session['cart'] = {}

    return render(request, 'checkout/order_success.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'checkout/order_history.html', {'orders': orders})


# Deprecated or Unused Views (deside whether to keep or remove after testing)

# def process_payment(request):
#     currency = request.session.get('currency', 'gbp')
#     amount = calculate_order_amount(request)

#     try:
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         intent = stripe.PaymentIntent.create(
#             amount=amount,  # Amount in pence
#             currency=currency,
#             payment_method_types=["card"],
#         )
#         return render(request, 'payment.html', {'client_secret': intent.client_secret})
#     except stripe.error.StripeError:
#         messages.error(request, "An error occurred during payment processing.")
#         return redirect('checkout:checkout')