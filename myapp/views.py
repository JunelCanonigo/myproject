from django.contrib.auth import logout
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Drivers, CustomUser
from django.contrib.auth.hashers import make_password

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
            messages.error(request, 'Invalid username or password')
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

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':  # Ensure only admins access this page
        return redirect('userdashboard')

    if request.method == 'POST':
        # Update admin details
        username = request.POST.get('username', request.user.username)
        password = request.POST.get('password', '')

        user = request.user  # Current admin user
        user.username = username

        if password:
            user.set_password(password)  # Update password if provided

        user.save()
        messages.success(request, 'Admin details updated successfully!')
        return redirect('admindashboard')  # Redirect to the same page after updating

    return render(request, 'admin_dashboard.html')  # Render admin edit page

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

@login_required
def update_admin_details(request):
    if request.method == "POST":
        # Get the logged-in user
        user = request.user
        
        # Get the username and password from the form
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')
        
        # Update the username
        if new_username and new_username != user.username:
            user.username = new_username
        
        # Update the password if a new one is provided
        if new_password:
            user.password = make_password(new_password)  # Hash the password
        
        # Save the updated user
        user.save()
        
        # Redirect to a success page or dashboard
        messages.success(request, "Your details have been updated successfully.")
        return redirect('admindashboard')  # Replace with the appropriate URL name for your dashboard

    return render(request, 'admin_dashboard.html')

#FETCHES ALL USERS
@login_required
def admindashboard(request):
    users = CustomUser.objects.exclude(is_staff=True, is_superuser=True) # Exclude users who are superusers (i.e., admins)
    return render(request, 'admin_dashboard.html', {'users': users})

@login_required
def update_user_details(request):
    if request.method == 'POST':
        # Get the current user
        user = request.user
        
        # Get the submitted username and password
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')
        
        # Check if the username has changed
        if new_username and new_username != user.username:
            user.username = new_username
        
        # Check if a new password was provided
        if new_password:
            # If password is provided, hash it before saving
            user.password = make_password(new_password)
        
        # Save the updated user data
        user.save()
        
        # Display a success message
        messages.success(request, "Your details have been updated successfully.")
        return redirect('userdashboard')  # Redirect back to the dashboard
    
    return render(request, 'user_dashboard.html')

@login_required
def current_user_info(request):
    # Retrieve the current user's information
    user = request.user

    # Prepare the context with user information
    context = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'role': user.role,  # Assuming your CustomUser model has a `role` field
    }

    

    return render(request, 'user_dashboard.html', context)