from .models import User

from django.shortcuts import render, redirect
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # If 'age' is not provided in the form data, set it to None
            age = form.cleaned_data.get('age', None)

            # Create user object without age
            user = form.save(commit=False)
            user.age = age
            print("user attachment successful")
            if user:
                # User was created successfully
                # Access the user details
                username = user.mail
                password = user.password
                # You can access other attributes of the user as well
                return redirect('registration_success')
        else:
            # User creation failed
            # Handle the failure appropriately
            # For example, you can return an error message or render a different template
            print("User creation failed.")
            print(form.errors)
    else:
        print("failed action")
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def registration_success(request):
    return render(request, 'regpass.html')
