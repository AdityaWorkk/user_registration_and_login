from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm

# User Registration
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash password
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to a dashboard or homepage
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'accounts/login.html')

# User Logout
def user_logout(request):
    logout(request)
    return redirect('login')

# Dashboard (Protected Page)
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

