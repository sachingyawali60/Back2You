from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
#login Logic

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')   # after login
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

#logout logic 

from django.contrib.auth import logout

def logout_user(request):
    logout(request)
    return redirect('login')

#Register 

def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Password match check
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        # Username exists check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        # Email exists check
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.save()

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'register.html')
