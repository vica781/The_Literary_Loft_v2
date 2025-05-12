from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from books.models import Book
from .forms import OrderForm, CustomUserChangeForm
from .models import Order, OrderItem, UserProfile

import stripe


# Main checkout view
def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(
            request,
            "Your bag is empty. Please add items before checkout."
        )
        return redirect('books:book_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            if request.user.is_authenticated:
                order.user = request.user
                save_info = 'save_info' in request.POST
                set_default_info = 'set_default_info' in request.POST

                if save_info:
                    request.session['delivery_info'] = {
                        'full_name': form.cleaned_data['full_name'],
                        'phone_number': form.cleaned_data['phone_number'],
                        'country': form.cleaned_data['country'],
                        'postcode': form.cleaned_data['postcode'],
                        'town_or_city': form.cleaned_data['town_or_city'],
                        'street_address1':
                            form.cleaned_data['street_address1'],
                        'street_address2':
                            form.cleaned_data['street_address2'],
                        'county': form.cleaned_data['county'],
                    }

                if set_default_info:
                    try:
                        profile = UserProfile.objects.get(user=request.user)
                        profile.default_full_name = form.cleaned_data[
                            'full_name']
                        profile.default_phone_number = form.cleaned_data[
                            'phone_number']
                        profile.default_country = form.cleaned_data['country']
                        profile.default_postcode = form.cleaned_data[
                            'postcode']
                        profile.default_town_or_city = form.cleaned_data[
                            'town_or_city']
                        profile.default_street_address1 = form.cleaned_data[
                            'street_address1']
                        profile.default_street_address2 = form.cleaned_data[
                            'street_address2']
                        profile.default_county = form.cleaned_data['county']
                        profile.save()
                    except UserProfile.DoesNotExist:
                        UserProfile.objects.create(
                            user=request.user,
                            default_full_name=form.cleaned_data['full_name'],
                            default_phone_number=form.cleaned_data[
                                'phone_number'],
                            default_country=form.cleaned_data['country'],
                            default_postcode=form.cleaned_data['postcode'],
                            default_town_or_city=form.cleaned_data[
                                'town_or_city'],
                            default_street_address1=form.cleaned_data[
                                'street_address1'],
                            default_street_address2=form.cleaned_data[
                                'street_address2'],
                            default_county=form.cleaned_data['county'],
                        )
            else:
                order.guest_email = form.cleaned_data['email']
                request.session['guest_order_number'] = str(order.order_number)

            total = 0
            for book_id, item_data in bag.items():
                try:
                    book = Book.objects.get(id=book_id)
                    quantity = item_data['quantity']
                    total += quantity * float(item_data['price'])
                except Book.DoesNotExist:
                    messages.error(
                        request,
                        f"Book with ID {book_id} was not found in database."
                    )
                    order.delete()
                    return redirect('books:view_cart')

            delivery_cost = (
                total * settings.STANDARD_DELIVERY_COST / 100
                if total < settings.FREE_DELIVERY_THRESHOLD else 0
            )

            order.order_total = total
            order.delivery_cost = delivery_cost
            order.grand_total = total + delivery_cost
            order.save()

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
                    messages.error(
                        request,
                        f"Book with ID {book_id} was not found in database."
                    )
                    order.delete()
                    return redirect('books:view_cart')

            request.session['bag'] = {}

            return redirect(
                'checkout:checkout_success',
                order_number=order.order_number
            )
        else:
            messages.error(
                request,
                "There was an error with your form. Please check your info."
            )
    else:
        form = OrderForm()
        if request.user.is_authenticated:
            try:
                delivery_info = request.session.get('delivery_info', {})
                try:
                    profile = UserProfile.objects.get(user=request.user)
                    initial_data = {
                        'full_name': delivery_info.get('full_name') or
                        profile.default_full_name or
                        request.user.get_full_name(),
                        'email': request.user.email,
                        'phone_number': delivery_info.get('phone_number') or
                        profile.default_phone_number or '',
                        'country': delivery_info.get('country') or
                        profile.default_country or '',
                        'postcode': delivery_info.get('postcode') or
                        profile.default_postcode or '',
                        'town_or_city': delivery_info.get('town_or_city') or
                        profile.default_town_or_city or '',
                        'street_address1': delivery_info.get(
                            'street_address1'
                            )
                        or profile.default_street_address1 or '',
                        'street_address2': delivery_info.get('street_address2')
                        or profile.default_street_address2 or '',
                        'county': delivery_info.get('county') or
                        profile.default_county or '',
                    }
                    form = OrderForm(
                        initial={k: v for k, v in initial_data.items() if v}
                    )
                except UserProfile.DoesNotExist:
                    if delivery_info:
                        form = OrderForm(initial=delivery_info)
                    else:
                        form = OrderForm(initial={
                            'full_name': request.user.get_full_name(),
                            'email': request.user.email
                        })
            except Exception as e:
                print(f"Error pre-filling form: {e}")
                form = OrderForm(initial={
                    'full_name': request.user.get_full_name(),
                    'email': request.user.email
                })

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
            messages.error(
                request,
                "A book in your bag was not found in our database."
            )
            return redirect('books:view_cart')

    delivery = (
        total * settings.STANDARD_DELIVERY_COST / 100
        if total < settings.FREE_DELIVERY_THRESHOLD else 0
    )
    grand_total = total + delivery

    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(grand_total * 100),
            currency=settings.STRIPE_CURRENCY,
        )
        client_secret = intent.client_secret
    except Exception as e:
        messages.error(request, f"Payment processing error: {str(e)}")
        return redirect('books:view_cart')

    context = {
        'order_form': form,
        'cart_items': cart_items,
        'total': total,
        'delivery': delivery,
        'grand_total': grand_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': client_secret,
    }

    return render(request, 'checkout/checkout.html', context)


def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    try:
        subject = f"Your Order Confirmation - {order.order_number}"
        context = {
            'order': order,
            'contact_email': settings.DEFAULT_FROM_EMAIL,
        }

        body = render_to_string(
            'checkout/emails/order_confirmation.txt',
            context
        )
        html_body = render_to_string(
            'checkout/emails/order_confirmation.html',
            context
        )

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            html_message=html_body,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Email sending failed: {e}")

    messages.success(
        request,
        f"Thank you for your order! A confirmation email has been sent "
        f"to {order.email}. Your order number is {order.order_number}."
    )

    context = {'order': order}
    return render(request, 'checkout/order_success.html', context)
