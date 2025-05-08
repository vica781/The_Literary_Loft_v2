from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout, name='checkout'),  # Checkout page
    path('wh/', views.stripe_webhook, name='stripe_webhook'),  # Stripe webhook
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),  # Cache checkout data
    # path('order-success/<uuid:order_number>/', views.order_success, name='order_success'),  # Order success page with UUID
    path('order-success/<str:order_number>/', views.order_success, name='order_success'),  # Order success page with order number
    path('order-history/', views.order_history, name='order_history'),  # Order history page
    path('my-account/', views.my_account, name='my_account'),  # My Account page
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('guest-order-lookup/', views.guest_order_lookup, name='guest_order_lookup'),
    path('debug/', views.debug_checkout, name='debug_checkout'),    
    
     # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='checkout/password_reset.html',
        email_template_name='checkout/password_reset_email.html',
        success_url='/checkout/password_reset/done/'),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='checkout/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='checkout/password_reset_confirm.html',
        success_url='/checkout/reset/done/'),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='checkout/password_reset_complete.html'),
         name='password_reset_complete'),
]
