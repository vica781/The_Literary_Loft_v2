from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout, name='checkout'),  # Checkout page
    path('wh/', views.stripe_webhook, name='stripe_webhook'),  # Stripe webhook
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),  # Cache checkout data
    path('order-success/<uuid:order_number>/', views.order_success, name='order_success'),  # Order success page with UUID
    path('order-history/', views.order_history, name='order_history'),  # Order history page
    path('my-account/', views.my_account, name='my_account'),  # My Account page
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
