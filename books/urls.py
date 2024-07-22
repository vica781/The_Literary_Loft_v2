from django.urls import path
from . import views

app_name = 'books'  # Define the namespace
urlpatterns = [
    path('', views.index, name='index'),  # 'index' view for the homepage
    path('shop/', views.shop, name='shop'),  # 'shop' view for the Shop page
    path('about/', views.about, name='about'),  # 'about' view for About Us page
    path('contact/', views.contact, name='contact'),  # 'contact' view for Contact Us page
]
