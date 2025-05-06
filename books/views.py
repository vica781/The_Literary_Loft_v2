# Standard Library Imports

# Django Imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.db.models import Q
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings

# Local App Imports
from .models import Book, Category, Subcategory, Newsletter
from .forms import BookForm


User = get_user_model()

# Check if the user is a staff admin
def is_admin(user):
    return user.is_staff


# ==================== Admin Book Management ====================

@user_passes_test(is_admin)
def add_book(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully!")
            return redirect('books:book_list')
        messages.error(request, "There was an error adding the book. Please check the form.")
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {
        'form': form,
        'categories': categories,
        'subcategories': subcategories,
    })


@user_passes_test(is_admin)
def edit_book(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully!")
            return redirect('books:book_list')
        messages.error(request, "There was an error updating the book.")
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit_book.html', {
        'form': form,
        'book': book,
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
    })


@user_passes_test(is_admin)
def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        confirmation = request.POST.get('confirmation', '').strip()
        if confirmation == book.title:
            book.delete()
            messages.success(request, f"Book '{book.title}' has been deleted.")
            return redirect('books:book_list')
        messages.error(request, "Confirmation failed. Title did not match.")
    return render(request, 'books/delete_book.html', {'book': book})


# ==================== User Authentication ====================

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        login(request, user)
        messages.success(request, f"Account created! Logged in as {user.username}")
        return redirect('books:index')

    return render(request, 'accounts/register.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            return redirect('books:index')
        messages.error(request, "Invalid email or password.")
    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('books:index')


# ==================== Static Pages ====================

def index(request):
    return render(request, 'books/index.html')

def about(request):
    return render(request, 'books/about.html')

def contact(request):
    return render(request, 'books/contact.html')


# ==================== Book Views ====================

def book_list(request, category_slug=None, subcategory_slug=None):
    books = Book.objects.all()
    category = subcategory = None

    if subcategory_slug:
        subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)
        books = books.filter(subcategory=subcategory)
    elif category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(subcategory__category=category)

    return render(request, 'books/book_list.html', {
        'books': books,
        'categories': Category.objects.all(),
        'category': category,
        'subcategory': subcategory,
    })


@login_required
def favorites_list(request):
    return render(request, 'books/favorites.html', {
        'favorite_books': request.user.favorite_books.all()
    })


def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'books/book_details.html', {'book': book})


# ==================== Search ====================

def search_suggestions(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(
        Q(title__icontains=query) | Q(author__icontains=query) | Q(isbn__icontains=query) | Q(subcategory__name__icontains=query)
    )[:15]
    suggestions = [{'id': b.id, 'title': b.title, 'author': b.author} for b in books]
    return JsonResponse(suggestions, safe=False)


def search_books(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(
        Q(title__icontains=query) | Q(author__icontains=query) | Q(isbn__icontains=query)
    ) if query else Book.objects.all()
    return render(request, 'books/search_results.html', {'books': books, 'query': query})


# ==================== Cart ====================

def add_to_cart(request, book_id):
    if not request.session.session_key:
        request.session.create()

    book = get_object_or_404(Book, id=book_id)
    quantity = int(request.POST.get('quantity', 1))
    bag = request.session.get('bag', {})

    if str(book_id) in bag:
        bag[str(book_id)]['quantity'] += quantity
    else:
        bag[str(book_id)] = {'quantity': quantity, 'price': float(book.price)}

    request.session['bag'] = bag
    request.session.modified = True

    messages.success(request, f'Added {book.title} to your bag.')
    return redirect(request.META.get('HTTP_REFERER', 'books:book_list'))


def view_cart(request):
    bag = request.session.get('bag', {})
    cart_items = []
    total = 0

    for book_id, item in bag.items():
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
        bag = request.session.get('bag', {})

        if book_id in bag:
            if quantity > 0:
                bag[book_id]['quantity'] = quantity
                messages.success(request, "Cart updated.")
            else:
                del bag[book_id]
                messages.success(request, "Item removed.")
        request.session['bag'] = bag
    return redirect('books:view_cart')


def remove_from_cart(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        bag = request.session.get('bag', {})
        if book_id in bag:
            del bag[book_id]
            messages.success(request, "Item removed from cart.")
        request.session['bag'] = bag
    return redirect('books:view_cart')


# ==================== Favorites ====================

@require_POST
@login_required
def toggle_favorite(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user = request.user
    if user in book.favorited_by.all():
        book.favorited_by.remove(user)
        is_favorite = False
    else:
        book.favorited_by.add(user)
        is_favorite = True
    return JsonResponse({
        'is_favorite': is_favorite,
        'favorite_count': user.favorite_books.count()
    })


# ==================== Marketing Page ====================

def facebook_mockup(request):
    book = get_object_or_404(Book, title="Tomorrow, and Tomorrow, and Tomorrow")
    secret_history = get_object_or_404(Book, title="The Secret History")
    little_friend = get_object_or_404(Book, title="The Little Friend")
    goldfinch = get_object_or_404(Book, title="The Goldfinch")

    return render(request, 'marketing/facebook_mockup_page.html', {
        'book': book,
        'secret_history': secret_history,
        'little_friend': little_friend,
        'goldfinch': goldfinch,
    })


# ==================== Error Pages ====================

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_500_view(request):
    return render(request, '500.html', status=500)


# ==================== Newsletter Signup ====================

def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('newsletter-email')

        if not email:
            return JsonResponse({'status': 'error', 'message': 'Please provide an email address.'})

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'status': 'error', 'message': 'Invalid email address.'})

        if Newsletter.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'This email is already subscribed.'})

        Newsletter.objects.create(email=email)
        return JsonResponse({'status': 'success', 'message': 'Successfully subscribed to the newsletter!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


# ==================== Debug ====================

@user_passes_test(is_admin)
# def debug_session(request):
#     """Debug view to inspect session data (admin only)"""
#     if not request.session.session_key:
#         request.session.create()
#     output = f"<h1>Session ID: {request.session.session_key}</h1><ul>"
#     for key, value in dict(request.session).items():
#         output += f"<li><strong>{key}:</strong> {value}</li>"
#     output += "</ul>"
#     return HttpResponse(output)

def debug_session(request):
    """Debug view - minimal version to test functionality"""
    return HttpResponse("Session debug test - if you see this, the view is working")