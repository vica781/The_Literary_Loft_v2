from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from .models import Order, OrderItem
from books.models import Book
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import stripe

# Main checkout view
def checkout(request):
    print(f"Checkout - Session ID: {request.session.session_key}")
    print(f"Bag contents at checkout: {request.session.get('bag', {})}")
    
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your bag is empty. Please add items before checkout.")
        return redirect('books:book_list')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            
            # If user is authenticated, associate the order with their account
            if request.user.is_authenticated:
                order.user = request.user
            
            order.save()
            
            # Create order line items
            total = 0
            for book_id, item_data in bag.items():
                try:
                    book = Book.objects.get(id=book_id)
                    quantity = item_data['quantity']
                    order_line_item = OrderItem(
                        order=order,
                        book=book,
                        quantity=quantity,
                    )
                    order_line_item.save()
                    total += item_data['quantity'] * float(item_data['price'])
                except Book.DoesNotExist:
                    messages.error(request, f"Book with ID {book_id} was not found in our database.")
                    order.delete()
                    return redirect('books:view_cart')
            
            # Update order total
            order.order_total = total
            order.save()
            
            # Clear the shopping bag
            request.session['bag'] = {}
            
            # Success message and redirect to thank you page
            messages.success(request, f"Order successfully placed! Your order number is {order.order_number}")
            return redirect('checkout:checkout_success', order_number=order.order_number)
        else:
            messages.error(request, "There was an error with your form. Please check your information.")
    else:
        # Create empty form for GET requests
        form = OrderForm()
        
        if request.user.is_authenticated:
            # Pre-fill the form with user information if available
            try:
                form = OrderForm(initial={
                    'full_name': request.user.get_full_name(),
                    'email': request.user.email,
                })
            except:
                pass
    
    # Get items from bag
    cart_items = []
    total = 0
    for book_id, item in bag.items():
        try:
            book = Book.objects.get(id=int(book_id))
            item_total = item['quantity'] * float(item['price'])
            total += item_total
            cart_items.append({
                'book': book,
                'quantity': item['quantity'],
                'price': item['price'],
                'total': item_total
            })
        except Book.DoesNotExist:
            messages.error(request, f"A book in your bag was not found in our database.")
            return redirect('books:view_cart')
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'total': total,
    }
    
    return render(request, 'checkout/checkout.html', context)

def order_success(request, order_number):
    """Handle successful checkouts"""
    order = get_object_or_404(Order, order_number=order_number)
    
    messages.success(request, f"Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.")
    
    context = {
        'order': order,
    }
    
    return render(request, 'checkout/checkout_success.html', context)


def handle_successful_payment(payment_intent):
    """
    Handle successful Stripe payments
    """
    # For now, just a placeholder that logs the payment ID
    print(f"Payment succeeded! Payment ID: {payment_intent['id']}")
    # Implement actual payment handling logic later
    return


def cache_checkout_data(request):
    """Temporary placeholder for cache checkout data handler"""
    return HttpResponse(status=200)


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
        handle_successful_payment(payment_intent)

    return HttpResponse(status=200)


def debug_checkout(request):
    """Temporary view to debug and fix checkout issues"""
    # Get the current bag data
    bag = request.session.get('bag', {})
    cart = request.session.get('cart', {})
    
    print(f"DEBUG - Session ID: {request.session.session_key}")
    print(f"DEBUG - Bag contents: {bag}")
    print(f"DEBUG - Cart contents: {cart}")
    
    # If bag is empty but cart has items, copy cart to bag
    if not bag and cart:
        print("DEBUG - Copying cart to bag")
        request.session['bag'] = cart.copy()
        request.session.modified = True
    
    return redirect('checkout:checkout')