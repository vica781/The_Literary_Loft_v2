from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm, CustomUserChangeForm
from .models import Order, OrderItem, UserProfile
from books.models import Book
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse 
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

import stripe

# Main checkout view
def checkout(request):    
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
                
                # Handle the checkboxes for saving delivery information
                save_info = 'save_info' in request.POST
                set_default_info = 'set_default_info' in request.POST
                
                # Save form data to session if 'save_info' is checked
                if save_info:
                    request.session['delivery_info'] = {
                        'full_name': form.cleaned_data['full_name'],
                        'phone_number': form.cleaned_data['phone_number'],
                        'country': form.cleaned_data['country'],
                        'postcode': form.cleaned_data['postcode'],
                        'town_or_city': form.cleaned_data['town_or_city'],
                        'street_address1': form.cleaned_data['street_address1'],
                        'street_address2': form.cleaned_data['street_address2'],
                        'county': form.cleaned_data['county'],
                    }
                
                # Update user profile with default address if 'set_default_info' is checked
                if set_default_info:
                    try:
                        profile = UserProfile.objects.get(user=request.user)
                        profile.default_full_name = form.cleaned_data['full_name']
                        profile.default_phone_number = form.cleaned_data['phone_number']
                        profile.default_country = form.cleaned_data['country']
                        profile.default_postcode = form.cleaned_data['postcode']
                        profile.default_town_or_city = form.cleaned_data['town_or_city']
                        profile.default_street_address1 = form.cleaned_data['street_address1']
                        profile.default_street_address2 = form.cleaned_data['street_address2']
                        profile.default_county = form.cleaned_data['county']
                        profile.save()
                    except UserProfile.DoesNotExist:
                        # Create a new profile if it doesn't exist
                        UserProfile.objects.create(
                            user=request.user,
                            default_full_name=form.cleaned_data['full_name'],
                            default_phone_number=form.cleaned_data['phone_number'],
                            default_country=form.cleaned_data['country'],
                            default_postcode=form.cleaned_data['postcode'],
                            default_town_or_city=form.cleaned_data['town_or_city'],
                            default_street_address1=form.cleaned_data['street_address1'],
                            default_street_address2=form.cleaned_data['street_address2'],
                            default_county=form.cleaned_data['county'],
                        )
            else:
                order.guest_email = form.cleaned_data['email']
                # Store order number in session for guest users
                request.session['guest_order_number'] = str(order.order_number)
            
            # Calculate totals
            total = 0
            for book_id, item_data in bag.items():
                try:
                    book = Book.objects.get(id=book_id)
                    quantity = item_data['quantity']
                    total += quantity * float(item_data['price'])
                except Book.DoesNotExist:
                    messages.error(request, f"Book with ID {book_id} was not found in our database.")
                    order.delete()
                    return redirect('books:view_cart')
            
            # Calculate delivery cost as a percentage of the order total
            if total < settings.FREE_DELIVERY_THRESHOLD:
                delivery_cost = total * settings.STANDARD_DELIVERY_COST / 100
            else:
                delivery_cost = 0
                
            # Update order totals
            order.order_total = total
            order.delivery_cost = delivery_cost
            order.grand_total = total + delivery_cost
            order.save()
            
            # Create order line items
            for book_id, item_data in bag.items():
                try:
                    book = Book.objects.get(id=book_id)
                    quantity = item_data['quantity']
                    order_line_item = OrderItem(
                        order=order,
                        book=book,
                        quantity=quantity,
                        price=item_data['price']
                    )
                    order_line_item.save()
                except Book.DoesNotExist:
                    messages.error(request, f"Book with ID {book_id} was not found in our database.")
                    order.delete()
                    return redirect('books:view_cart')
            
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
            # Try to pre-fill the form with user information
            try:
                # First check if there's saved information in the session
                delivery_info = request.session.get('delivery_info', {})
                
                # Then try to get the user profile
                try:
                    profile = UserProfile.objects.get(user=request.user)
                    
                    # Create initial data dictionary with user info
                    initial_data = {
                        'full_name': delivery_info.get('full_name') or profile.default_full_name or request.user.get_full_name(),
                        'email': request.user.email,
                        'phone_number': delivery_info.get('phone_number') or profile.default_phone_number or '',
                        'country': delivery_info.get('country') or profile.default_country or '',
                        'postcode': delivery_info.get('postcode') or profile.default_postcode or '',
                        'town_or_city': delivery_info.get('town_or_city') or profile.default_town_or_city or '',
                        'street_address1': delivery_info.get('street_address1') or profile.default_street_address1 or '',
                        'street_address2': delivery_info.get('street_address2') or profile.default_street_address2 or '',
                        'county': delivery_info.get('county') or profile.default_county or '',
                    }
                    
                    # Use only non-empty values
                    form = OrderForm(initial={k: v for k, v in initial_data.items() if v})
                    
                except UserProfile.DoesNotExist:
                    # If no profile exists, try to use session data
                    if delivery_info:
                        form = OrderForm(initial={
                            'full_name': delivery_info.get('full_name', request.user.get_full_name()),
                            'email': request.user.email,
                            'phone_number': delivery_info.get('phone_number', ''),
                            'country': delivery_info.get('country', ''),
                            'postcode': delivery_info.get('postcode', ''),
                            'town_or_city': delivery_info.get('town_or_city', ''),
                            'street_address1': delivery_info.get('street_address1', ''),
                            'street_address2': delivery_info.get('street_address2', ''),
                            'county': delivery_info.get('county', ''),
                        })
                    else:
                        # Fallback to basic user info
                        form = OrderForm(initial={
                            'full_name': request.user.get_full_name(),
                            'email': request.user.email,
                        })
            except Exception as e:
                # If any errors occur, just use basic user info
                print(f"Error pre-filling form: {e}")
                form = OrderForm(initial={
                    'full_name': request.user.get_full_name(),
                    'email': request.user.email,
                })
    
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
    
    # Calculate delivery cost
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * settings.STANDARD_DELIVERY_COST / 100
    else:
        delivery = 0
    
    grand_total = total + delivery
    
    # Create Stripe payment intent
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(grand_total * 100),  # Convert to pence for Stripe
            currency=settings.STRIPE_CURRENCY,
        )
        client_secret = intent.client_secret
    except Exception as e:
        messages.error(request, f"Payment processing error: {str(e)}")
        return redirect('books:view_cart')
    
    # Create context with ALL needed variables
    context = {
        'order_form': form,  # Use the existing form variable
        'cart_items': cart_items,
        'total': total,
        'delivery': delivery,
        'grand_total': grand_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': client_secret,
    }
    
    return render(request, 'checkout/checkout.html', context)


def order_success(request, order_number):
    """Handle successful checkouts"""
    order = get_object_or_404(Order, order_number=order_number)
    
    print(f"Processing successful order: {order_number}")
    
    # Send the order confirmation email
    try:
        from django.template.loader import render_to_string
        from django.conf import settings
        
        subject = f"Your Order Confirmation - {order.order_number}"
        context = {
            'order': order,
            'contact_email': settings.DEFAULT_FROM_EMAIL,
        }
        
        body = render_to_string('checkout/emails/order_confirmation.txt', context)
        html_body = render_to_string('checkout/emails/order_confirmation.html', context)
        
        print(f"Attempting to send email to: {order.email}")
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            html_message=html_body,
            fail_silently=False,
        )
        
        print(f"Email sent successfully to: {order.email}")
    except Exception as e:
        # Log the error but don't disrupt the user experience
        print(f"Email sending failed: {e}")
    
    messages.success(request, f"Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email has been sent to {order.email}.")
    
    context = {
        'order': order,
    }
    
    return render(request, 'checkout/order_success.html', context)


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
def update_default_address(request):
    if request.method == 'POST':
        # Get user profile
        profile = UserProfile.objects.get(user=request.user)
        
        # Update profile with form data
        profile.default_phone_number = request.POST.get('default_phone_number', '')
        profile.default_street_address1 = request.POST.get('default_street_address1', '')
        profile.default_street_address2 = request.POST.get('default_street_address2', '')
        profile.default_town_or_city = request.POST.get('default_town_or_city', '')
        profile.default_county = request.POST.get('default_county', '')
        profile.default_postcode = request.POST.get('default_postcode', '')
        profile.default_country = request.POST.get('default_country', '')
        
        profile.save()
        
        messages.success(request, 'Default delivery address updated successfully')
        return redirect('checkout:my_account')
    
    return redirect('checkout:my_account')

@login_required
def clear_default_address(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        
        # Clear all default address fields
        profile.default_phone_number = ''
        profile.default_street_address1 = ''
        profile.default_street_address2 = ''
        profile.default_town_or_city = ''
        profile.default_county = ''
        profile.default_postcode = ''
        profile.default_country = ''
        
        profile.save()
        
        messages.success(request, 'Default delivery address has been cleared')
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found')
    
    return redirect('checkout:my_account')

@login_required
def clear_saved_info(request):
    if 'delivery_info' in request.session:
        del request.session['delivery_info']
        messages.success(request, 'Temporarily saved delivery information has been cleared')
    else:
        messages.info(request, 'No saved delivery information found')
    
    return redirect('checkout:my_account')


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