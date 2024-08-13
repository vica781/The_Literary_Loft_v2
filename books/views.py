from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.contrib.auth import logout
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Book, Category, Subcategory
from django.conf import settings
import stripe


# USER REGISTRATION / LOGIN / LOGOUT
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

# HOME PAGE / ABOUT / CONTACT
def index(request):
    """ A view that displays the home page """    
    return render(request, 'books/index.html')

def about(request):
    """ A view that displays the about page """
    return render(request, 'books/about.html')

def contact(request):
    """ A view that displays the contact page """
    return render(request, 'books/contact.html')

# BOOK LIST / BOOK DETAIL
def book_list(request, category_slug=None, subcategory_slug=None):
    books = Book.objects.all()
    categories = Category.objects.all()
    category = None
    subcategory = None

    if subcategory_slug:
        subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)
        books = books.filter(subcategory=subcategory)
    
    elif category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(subcategory__category=category)

    context = {
        'books': books,
        'categories': categories,
        'category': category,
        'subcategory': subcategory,
    }
    return render(request, 'books/book_list.html', context)

    
    
def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'books/book_details.html', {'book': book})

def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # Here add the logic to add the book to the cart
    # For now, just redirect back to the book detail page
    return redirect('books:book_detail', id=book_id)

def search_books(request):
    query = request.GET.get('q')
    books = Book.objects.filter(
        Q(title__icontains=query) | Q(author__icontains=query) | Q(isbn__icontains=query)
    ) if query else Book.objects.all()
    return render(request, 'books/search_results.html', {'books': books, 'query': query})

# PAYMENT PROCESS
def calculate_order_amount(request):
    cart = request.session.get('cart', {})
    total = 0
    for item in cart.values():
        total += item['price'] * item['quantity']
    return int(total * 100)  # Convert GBP to pence

def process_payment(request):
    currency = request.session.get('currency', 'gbp')  # Default to GBP
    amount = calculate_order_amount(request)
    
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount=amount,  # Amount in pence
            currency=currency,
            payment_method_types=["card"],
        )
        return render(request, 'payment.html', {'client_secret': intent.client_secret})
    except stripe.error.StripeError as e:
        # Handle error
        messages.error(request, "An error occurred during payment processing.")
        return redirect('books:checkout')  # Adjust redirect as needed

