from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_order_confirmation_email(order, to_email):
    subject = f"Your Order Confirmation - {order.order_number}"
    context = {
        'order': order,
        'contact_email': settings.DEFAULT_FROM_EMAIL,
    }
    body = render_to_string('checkout/emails/order_confirmation.txt', context)
    html_body = render_to_string(
        'checkout/emails/order_confirmation.html',
        context
        )

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        html_message=html_body,
        fail_silently=False,
    )
