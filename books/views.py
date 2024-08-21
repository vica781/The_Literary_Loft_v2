from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.db.models import Q
from .models import Book, Category, Subcategory
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


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

# SEARCH BOOKS
def search_suggestions(request):
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query) | Q(isbn__icontains=query) | 
            Q(subcategory__name__icontains=query)
        )[:15]  # Limit to 15 suggestions
        suggestions = [{'id': book.id, 'title': book.title, 'author': book.author} for book in books]
        return JsonResponse(suggestions, safe=False)
    return JsonResponse([], safe=False)

def search_books(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(
        Q(title__icontains=query) | Q(author__icontains=query) | Q(isbn__icontains=query)
    ) if query else Book.objects.all()
    
    context = {
        'books': books,
        'query': query
    }
    return render(request, 'books/search_results.html', context)
       
def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'books/book_details.html', {'book': book})

# CART FUNCTIONALITY
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 1))

    if str(book_id) in cart:
        cart[str(book_id)]['quantity'] += quantity
    else:
        cart[str(book_id)] = {'quantity': quantity, 'price': float(book.price)}

    request.session['cart'] = cart
    messages.success(request, f'Added {book.title} to your bag')
    return redirect(request.META.get('HTTP_REFERER', 'books:book_list'))

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for book_id, item in cart.items():
        book = Book.objects.get(id=int(book_id))
        item_total = item['quantity'] * float(item['price'])
        total += item_total
        cart_items.append({
            'book': book,
            'quantity': item['quantity'],
            'price': item['price'],
            'total': item_total
        })
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total': total})

def update_cart(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        quantity = int(request.POST.get('quantity'))
        
        cart = request.session.get('cart', {})
        
        if book_id in cart:
            if quantity > 0:
                cart[book_id]['quantity'] = quantity
                messages.success(request, "Cart updated successfully.")
            else:
                del cart[book_id]
                messages.success(request, "Item removed from cart.")
        
        request.session['cart'] = cart
    return redirect('books:view_cart')

def remove_from_cart(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        
        cart = request.session.get('cart', {})
        
        if book_id in cart:
            del cart[book_id]
            messages.success(request, "Item removed from cart.")
        
        request.session['cart'] = cart
    return redirect('books:view_cart')
