from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
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
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There is nothing in your bag at the moment. \
            Please, add items to your bag before checking out.")
        return redirect('books:book_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            total = calculate_order_amount(request) / 100  # Convert back to pounds
            order.order_total = total
            
            # Calculate delivery cost
            if total < settings.FREE_DELIVERY_THRESHOLD:
                delivery_cost = total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
            else:
                delivery_cost = 0
            
            order.delivery_cost = delivery_cost
            order.grand_total = total + delivery_cost
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
            
            return redirect('checkout:order_success')
    else:
        form = OrderForm()

    # Calculate total and create PaymentIntent
    if not settings.STRIPE_PUBLIC_KEY:
        messages.error(request, "Stripe public key is missing. \
            Make sure you have set it in your environment variables.")
        return redirect('checkout:checkout')
    
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

    # Calculate delivery cost
    if total_display < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total_display * settings.STANDARD_DELIVERY_PERCENTAGE / 100
    else:
        delivery = 0

    grand_total = total_display + delivery

    context = {
        'order_form': form,
        'cart_items': cart_items,
        'total': total_display,
        'delivery': delivery,
        'grand_total': grand_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context)

@require_POST
@csrf_exempt
def cache_checkout_data(request):
    try:
        # Retrieve the payment intent ID and other data
        payment_intent_id = request.POST.get('client_secret').split('_secret')[0]
        save_info = request.POST.get('save_info')

        # Optionally update the payment intent with additional metadata
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(
            payment_intent_id,
            metadata={
                'user': request.user.id,
                'save_info': save_info,
                'cart': str(request.session.get('cart', {}))
            }
        )

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

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
        return render(request, 'checkout/order_success.html')

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
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'checkout/order_history.html', {'orders': orders})
