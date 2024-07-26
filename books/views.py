from django.shortcuts import render

# Create your views here.

def index(request):
    """ A view that displays the index page """    
    return render(request, 'books/index.html')

def shop(request):
    """ A view that displays the shop page """
    return render(request, 'books/shop.html')

def about(request):
    """ A view that displays the about page """
    return render(request, 'books/about.html')

def contact(request):
    """ A view that displays the contact page """
    return render(request, 'books/contact.html')
def login(request):
    """ A view that displays the login page """
    return render(request, 'accounts/login.html')