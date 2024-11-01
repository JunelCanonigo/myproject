from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required  # Import the login_required decorator
from django.contrib import messages  # Import the messages framework
from .models import Drivers  # Import your Drivers model

def landing_page(request):
    return render(request, 'landing.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')  # Redirect to the dashboard after successful login
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'registration/login.html')

def register_page(request):
    if request.method == 'POST':
        # Retrieve data from the form
        username = request.POST['username']
        password = request.POST['password']
        plate_number = request.POST['plate_number']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email_address = request.POST.get('email_address', '')  # Default to empty string if not provided
        phone_number = request.POST['phone_number']
        address = request.POST['address']

        # Create a new user instance
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email_address)
        
        # Create a new driver instance
        driver = Drivers(
            plate_number=plate_number,
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            phone_number=phone_number,
            address=address,
            user=user  # Assuming the Drivers model has a foreign key to User
        )
        
        # Save the driver to the database
        driver.save()

        messages.success(request, 'You have successfully registered!')
        return redirect('login_page')  # Redirect to login after registration

    return render(request, 'registration/register.html')

def profile_page(request):
    return render(request, 'profile.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')




