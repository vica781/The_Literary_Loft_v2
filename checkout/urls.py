from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout, name='checkout'),  # Checkout page
    path('wh/', views.stripe_webhook, name='stripe_webhook'),  # Stripe webhook
]
