from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponse
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
    # Placeholder for processing logic when a payment is successful
    print(f"PaymentIntent {payment_intent['id']} was successful!")
    # Implement additional logic like updating order status, sending confirmation emails, etc.

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There is nothing in your bag at the moment. Please, add items to your bag before checking out.")
        return redirect('books:book_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            total = calculate_order_amount(request) / 100  # Convert back to pounds
            order.order_total = total

            # Calculate delivery cost as a percentage of the order total
            if total < settings.FREE_DELIVERY_THRESHOLD:
                delivery_cost = total * settings.STANDARD_DELIVERY_COST / 100  # Calculate as percentage
            else:
                delivery_cost = 0

            order.delivery_cost = delivery_cost
            order.grand_total = total + delivery_cost
            order.order_number = str(uuid.uuid4())
            order.save()

            for book_id, item in cart.items():
                book = get_object_or_404(Book, id=int(book_id))
                OrderItem.objects.create(
                    order=order,
                    book=book,
                    quantity=item['quantity'],
                    price=item['price']
                )

            # Clear the cart after a successful order
            request.session['cart'] = {}
            messages.success(request, "Order placed successfully.")

            # Redirect to the order success page with the order number
            return redirect('checkout:order_success', order_number=order.order_number)
    else:
        form = OrderForm()

    # Calculate total and create PaymentIntent
    total = calculate_order_amount(request) / 100  # Convert back to pounds
    delivery_cost = 0  # Default to 0 unless conditions require otherwise

    # If the total is less than the free delivery threshold, calculate the delivery cost as a percentage
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery_cost = total * settings.STANDARD_DELIVERY_COST / 100  # Calculate as percentage

    grand_total = total + delivery_cost

    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount=int(grand_total * 100),  # Convert back to pence for Stripe
            currency=settings.STRIPE_CURRENCY,
        )
    except stripe.error.StripeError:
        messages.error(request, "An error occurred while creating the payment intent.")
        return redirect('checkout:checkout')

    context = {
        'order_form': form,
        'cart_items': [{'book': get_object_or_404(Book, id=int(book_id)), 'quantity': item['quantity'], 'price': item['price'], 'total': item['quantity'] * float(item['price'])} for book_id, item in cart.items()],
        'total': total,
        'delivery': delivery_cost,  # Already in pounds
        'grand_total': grand_total,  # Already in pounds
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context)

@require_POST
@csrf_exempt
def cache_checkout_data(request):
    try:
        payment_intent_id = request.POST.get('client_secret').split('_secret')[0]
        save_info = request.POST.get('save_info')

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
def order_success(request, order_number):
    # Retrieve the existing order using the order_number
    order = get_object_or_404(Order, order_number=order_number)

    # Render the order success page with the order details
    return render(request, 'checkout/order_success.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'checkout/order_history.html', {'orders': orders})
