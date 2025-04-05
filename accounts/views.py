from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, EditProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from shop.models import Product ,Order, OrderItem


def login_page(request):
    next_page = request.GET.get('next')
    if request.user.is_authenticated:
        return redirect('shop:home_page')

    if request.method == "GET":
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if next_page:
                    return redirect(next_page)
                return redirect('shop:home_page')
    return render(request, 'accounts/login_page.html', context={'form': form})


def logout_page(request):
    next_page = request.GET.get('next')

    logout(request)
    if next_page:
        return redirect(next_page)
    return redirect('shop:home_page')


def register_page(request):
    next_page = request.GET.get('next')

    if request.user.is_authenticated:
        if next_page:
            return redirect(next)
        return redirect('shop:home_page')

    if request.method == "GET":
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password_1 = form.cleaned_data.get('password_1')
            user = User.objects.create_user(username=username, password=password_1, email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            login(request, user)
            if next_page:
                return redirect(next_page)
            return redirect('shop:home_page')
    return render(request, 'accounts/register_page.html', context={'form': form})


@login_required
def dashboard_page(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, 'accounts/dashboard/dashboard_page.html', context={'orders': orders})


@login_required
def edit_profile_page(request):
    if request.method == "GET":
        username = request.user.username
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        form = EditProfile(
            initial={'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email})
    else:
        form = EditProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:edit_profile_page')

    return render(request, 'accounts/dashboard/edit_profile.html', context={'form': form})


@login_required
def show_orders(request):

    orders = Order.objects.filter(user=request.user)

    return render(request, 'accounts/dashboard/order_page.html', context={'orders': orders})
