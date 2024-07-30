from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.backends import ModelBackend
from django.urls import reverse
from django.contrib.auth import logout


def index(request):
    """ A view that displays the home page """    
    return render(request, 'books/index.html')

def book_list(request):
    """ A view that displays the shop page """
    return render(request, 'books/book_list.html')

def about(request):
    """ A view that displays the about page """
    return render(request, 'books/about.html')

def contact(request):
    """ A view that displays the contact page """
    return render(request, 'books/contact.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, 'accounts/register.html')
        
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        
        messages.success(request, f"Account created successfully! You are logged in as {user.username}")
        return redirect('books:index')
    
    return render(request, 'accounts/register.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Logged in successfully as {user.username}")
            return redirect(reverse('books:index'))
        else:
            messages.error(request, "Invalid email or password")
    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('books:index')