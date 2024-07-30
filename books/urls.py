from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'books'  # Define the namespace

urlpatterns = [
    path('', views.index, name='index'),  # 'index' view for the homepage
    path('book_list/', views.book_list, name='book_list'),  # 'shop' view for the Shop page
    path('about/', views.about, name='about'),  # 'about' view for About Us page
    path('contact/', views.contact, name='contact'),  # 'contact' view for Contact Us page
    path('register/', views.register, name='register'),  # 'register' view for Register page    
    path('login/', views.user_login, name='login'), # 'login' view for Login page
    path('logout/', views.user_logout, name='logout'), # 'logout' view 
]