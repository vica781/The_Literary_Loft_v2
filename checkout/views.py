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
from .forms import OrderForm, CustomUserChangeForm
from .utils import send_order_confirmation_email


def calculate_order_amount(request):
    bag = request.session.get('bag', {})
    total = sum(item['price'] * item['quantity'] for item in bag.values())
    return int(total * 100)  # Convert GBP to pence


def handle_successful_payment_intent(payment_intent):
    print(f"PaymentIntent {payment_intent['id']} was successful!")


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your bag is empty. Please add items before checkout.")
        return redirect('books:book_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user

                save_info = request.POST.get('save_info')
                set_default_info = request.POST.get('set_default_info')

                if set_default_info == 'on' and hasattr(request.user, 'profile'):
                    try:
                        profile = request.user.profile
                        profile.default_full_name = form.cleaned_data['full_name']
                        profile.default_phone_number = form.cleaned_data['phone_number']
                        profile.default_country = form.cleaned_data['country']
                        profile.default_postcode = form.cleaned_data['postcode']
                        profile.default_town_or_city = form.cleaned_data['town_or_city']
                        profile.default_street_address1 = form.cleaned_data['street_address1']
                        profile.default_street_address2 = form.cleaned_data['street_address2']
                        profile.default_county = form.cleaned_data['county']
                        profile.save()
                        messages.success(request, "Your address has been saved for future purchases!")
                    except Exception as e:
                        messages.error(request, f"Error saving profile: {str(e)}")
            else:
                order.guest_email = form.cleaned_data['email']

            total = calculate_order_amount(request) / 100
            order.order_total = total
            order.delivery_cost = total * settings.STANDARD_DELIVERY_COST / 100 if total < settings.FREE_DELIVERY_THRESHOLD else 0
            order.grand_total = order.order_total + order.delivery_cost
            order.order_number = str(uuid.uuid4())
            order.save()

            for book_id, item in bag.items():
                book = get_object_or_404(Book, id=int(book_id))
                OrderItem.objects.create(
                    order=order,
                    book=book,
                    quantity=item['quantity'],
                    price=item['price']
                )

            recipient_email = order.email
            send_order_confirmation_email(order, recipient_email)

            if not request.user.is_authenticated:
                request.session['guest_order_number'] = order.order_number

            request.session['bag'] = {}
            messages.success(request, "Order placed successfully!")
            return redirect('checkout:order_success', order_number=order.order_number)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label or field}: {error}")
    else:
        if request.user.is_authenticated:
            try:
                if hasattr(request.user, 'profile'):
                    profile = request.user.profile
                    initial_data = {
                        'full_name': profile.default_full_name,
                        'phone_number': profile.default_phone_number,
                        'country': profile.default_country,
                        'postcode': profile.default_postcode,
                        'town_or_city': profile.default_town_or_city,
                        'street_address1': profile.default_street_address1,
                        'street_address2': profile.default_street_address2,
                        'county': profile.default_county,
                        'email': request.user.email,
                    }
                    form = OrderForm(initial=initial_data)
                else:
                    form = OrderForm(initial={'email': request.user.email})
            except Exception:
                form = OrderForm(initial={'email': request.user.email})
        else:
            form = OrderForm()

    total = calculate_order_amount(request) / 100
    delivery_cost = total * settings.STANDARD_DELIVERY_COST / 100 if total < settings.FREE_DELIVERY_THRESHOLD else 0
    grand_total = total + delivery_cost

    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount=int(grand_total * 100),
            currency=settings.STRIPE_CURRENCY,
        )
    except stripe.error.StripeError as e:
        messages.error(request, f"Payment processing error: {str(e)}")
        return redirect('checkout:checkout')

    bag = request.session.get('bag', {})
    request.session.modified = True

    context = {
        'order_form': form,
        'cart_items': [{
            'book': get_object_or_404(Book, id=int(book_id)),
            'quantity': item['quantity'],
            'price': item['price'],
            'total': item['quantity'] * float(item['price'])
        } for book_id, item in bag.items()],
        'total': total,
        'delivery': delivery_cost,
        'grand_total': grand_total,
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
                'user': request.user.id if request.user.is_authenticated else 'guest',
                'save_info': save_info,
                'bag': str(request.session.get('bag', {}))
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
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_successful_payment_intent(payment_intent)

    return HttpResponse(status=200)


def order_success(request, order_number):
    try:
        order = get_object_or_404(Order, order_number=order_number)
        
        if request.user.is_authenticated:
            if order.user != request.user:
                messages.error(request, "You don't have permission to view this order.")
                return redirect('books:index')
        else:
            if 'guest_order_number' not in request.session or request.session['guest_order_number'] != order_number:
                messages.error(request, "You don't have permission to view this order.")
                return redirect('books:index')
        
        if 'bag' in request.session:
            del request.session['bag']
        
        return render(request, 'checkout/order_success.html', {'order': order})
    except Exception as e:
        messages.error(request, f"Error retrieving order: {str(e)}")
        return redirect('books:index')


@login_required
def order_history(request):
    try:
        sort_by = request.GET.get('sort_by', 'date')
        sort_order = request.GET.get('sort_order', 'desc')
        
        if sort_order == 'asc':
            orders = Order.objects.filter(user=request.user).order_by(sort_by)
        else:
            orders = Order.objects.filter(user=request.user).order_by(f'-{sort_by}')

        return render(request, 'checkout/order_history.html', {
            'orders': orders,
            'sort_by': sort_by,
            'sort_order': sort_order,
        })
    except Exception as e:
        messages.error(request, f"Error retrieving order history: {str(e)}")
        return redirect('checkout:my_account')


@login_required
def my_account(request):
    try:
        orders = Order.objects.filter(user=request.user).order_by('-date')[:5]
        form = CustomUserChangeForm(instance=request.user)
        return render(request, 'checkout/my_account.html', {
            'orders': orders,
            'form': form,
        })
    except Exception as e:
        messages.error(request, f"Error loading account page: {str(e)}")
        return redirect('books:index')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('checkout:my_account')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label or field}: {error}")
    else:
        form = CustomUserChangeForm(instance=request.user)

    orders = Order.objects.filter(user=request.user).order_by('-date')[:5]
    return render(request, 'checkout/my_account.html', {
        'form': form,
        'orders': orders,
    })


def guest_order_lookup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        order_number = request.POST.get('order_number')
        
        try:
            order = Order.objects.get(guest_email=email, order_number=order_number)
            return render(request, 'checkout/guest_order_detail.html', {'order': order})
        except Order.DoesNotExist:
            messages.error(request, "No order found with the provided details.")
        except Exception as e:
            messages.error(request, f"Error retrieving order: {str(e)}")
    
    return render(request, 'checkout/guest_order_lookup.html')
