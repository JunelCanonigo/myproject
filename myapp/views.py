from django.contrib.auth import logout
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Drivers, CustomUser

# Landing Page
def landing_page(request):
    return render(request, 'landing.html')

# Login Page
def login_page(request):
    if request.user.is_authenticated:
        # Redirect to the appropriate dashboard based on the user role
        if request.user.role == 'admin':
            return redirect('admindashboard')  # Replace 'admindashboard' with your actual dashboard URL name
        else:
            return redirect('userdashboard')  # Replace 'userdashboard' with your actual dashboard URL name

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect based on user role
            if user.role == 'admin':
                return redirect('admindashboard')
            elif user.role == 'user':
                return redirect('userdashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'registration/login.html')
    
    return render(request, 'registration/login.html')

# Register Page
def register_page(request):
    if request.user.is_authenticated:
        # Redirect to the appropriate dashboard based on the user role
        if request.user.role == 'admin':
            return redirect('admindashboard')  # Replace 'admindashboard' with your actual dashboard URL name
        else:
            return redirect('userdashboard')  # Replace 'userdashboard' with your actual dashboard URL name

    if request.method == 'POST':
        # Retrieve data for the User model
        username = request.POST['username']
        password = request.POST['password']
        plate_number = request.POST['plate_number']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email_address = request.POST.get('email_address', '')  # Optional
        phone_number = request.POST['phone_number']
        address = request.POST['address']

        # Check if the username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'registration/register.html')

        # Create the User object
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email_address,
            first_name=first_name,
            last_name=last_name,
        )

        # Create the Drivers object linked to the User
        driver = Drivers.objects.create(
            user=user,  # Assuming your Drivers model has a OneToOneField to the User model
            plate_number=plate_number,
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            phone_number=phone_number,
            address=address
        )

        return redirect('login_page')  # Redirect to login after successful registration
    
    return render(request, 'registration/register.html')

# Profile Page
def profile_page(request):
    return render(request, 'profile.html')

# Dashboard Page
def dashboard(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'dashboard.html', context)

# Graphs View
def graphs_view(request):
    return render(request, 'graphs.html')

# Reports Page
def reports(request):
    return render(request, 'reports.html')

# Admin Dashboard - Protected by login_required and role check
@login_required
def admindashboard(request):
    if request.user.role != 'admin':  # If the logged-in user is not an admin, redirect to user dashboard
        return redirect('userdashboard')
    return render(request, 'admin_dashboard.html')

# User Dashboard - Protected by login_required and role check
@login_required
def userdashboard(request):
    # Check if the logged-in user is a regular user (role='user')
    if request.user.role != 'user':  
        # Redirect to admin dashboard if the user is not a regular user
        return redirect('admindashboard')
    return render(request, 'user_dashboard.html')
    

def logout_page(request):
    logout(request)  # This will log out the user from all sessions
    return redirect('dashboard')
