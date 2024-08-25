from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout, name='checkout'),  # Checkout page
    path('wh/', views.stripe_webhook, name='stripe_webhook'),  # Stripe webhook
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),  # Cache checkout data
    path('order-success/', views.order_success, name='order_success'),  # Order success page
    path('order-history/', views.order_history, name='order_history'),  # Add this line
]
