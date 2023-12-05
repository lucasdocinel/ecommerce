from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms


def category(request, foo):
    # Replace Hyphens with Spaces
    foo = foo.replace('-', ' ')
    # Grab th category from the url
    try:
        # Look up the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, "category.html", {'category': category, 'products': products})
    except:
        messages.success(request, ("Category Does Not Exist"))
        return redirect("home")


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, "product.html", {'product': product})


def home(request):
    products = Product.objects.all()
    return render(request, "home.html", {'products': products})


def about (request):
    return render(request, "about.html")

def login_user (request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect("home")
        else:
            messages.error(request, "Login Failed")
            return redirect("login")
    else:
        return render(request, "login.html", {})


def logout_user (request):
    logout(request)
    messages.success(request, "Logout Successful")
    return redirect("home")


def register_user (request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration Successful")
            return redirect("home")
        else:
            messages.error(request, "Registration Failed")
            return redirect("register")
    else:
        return render(request, "register.html", {'form': form})
    