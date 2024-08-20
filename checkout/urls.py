from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [ 
path('checkout/wh/', views.stripe_webhook, name='stripe_webhook'),
]