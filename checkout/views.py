from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserChangeForm

import stripe
import uuid

from .models import Order, OrderItem
from books.models import Book
from .forms import OrderForm, CustomUserChangeForm

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
            # handle both authenticated and guest users
            if request.user.is_authenticated:
                order.user = request.user
            else:
                order.guest_email = form.cleaned_data['email']
                
        if not request.user.is_authenticated:
            request.session['guest_order_number'] = str(order.order_number)
                
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

# ORDER-RELATED VIEWS
def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    
    if request.user.is_authenticated:
        if order.user != request.user:
            messages.error(request, "You don't have permission to view this order.")
            return redirect('books:index')  
    else:
        # For guest users, check if the order number is in the session
        if not order_number:  
            messages.error(request, "You don't have permission to view this order.")
            return redirect('books:index')  
    
    # Clear the cart
    if 'cart' in request.session:
        del request.session['cart']
    
    template = 'checkout/order_success.html'
    context = {
        'order': order,
    }
    
    return render(request, template, context)

@login_required
def order_history(request):
    sort_by = request.GET.get('sort_by', 'date')
    sort_order = request.GET.get('sort_order', 'desc')
    
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
    else:
        # For guest users, retrieve orders based on the stored order number
        guest_order_number = request.session.get('guest_order_number')
        orders = Order.objects.filter(order_number=guest_order_number) if guest_order_number else Order.objects.none()
        
    if sort_order == 'asc':
        orders = Order.objects.filter(user=request.user).order_by(sort_by)
    else:
        orders = Order.objects.filter(user=request.user).order_by(f'-{sort_by}')

    context = {
        'orders': orders,
        'sort_by': sort_by,
        'sort_order': sort_order,
    }

    return render(request, 'checkout/order_history.html', context)

@login_required
def my_account(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')
    form = CustomUserChangeForm(instance=request.user)
    context = {
        'orders': orders,
        'form': form,
    }
    return render(request, 'checkout/my_account.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('checkout:my_account')
    else:
        form = CustomUserChangeForm(instance=request.user)

    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'checkout/my_account.html', {'form': form, 'orders': orders})

# Add a new view for guest order lookup
def guest_order_lookup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        order_number = request.POST.get('order_number')
        
        try:
            order = Order.objects.get(guest_email=email, order_number=order_number)
            return render(request, 'checkout/guest_order_detail.html', {'order': order})
        except Order.DoesNotExist:
            messages.error(request, "No order found with the provided details.")
    
    return render(request, 'checkout/guest_order_lookup.html')