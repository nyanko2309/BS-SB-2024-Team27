from django.core.checks import templates
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from login.models import User
from django.shortcuts import render, redirect

from django.core.exceptions import ObjectDoesNotExist # for helper function

def login(request):
    currentid=0
    user = User.objects.get(id=2)  # Fetch the user with id 2
    HTML = render_to_string('Login.html')  # Render the template
    return HttpResponse(HTML)



def getIdByUserCredentials(mail, password) -> int | str:
    """returns id of a user after receiving mail and password, returns string of 'user doesn't exist' or 'mail or password are incorrect' otherwise"""
    userid = 2

    try:
        user = User.objects.get(id=userid)
    except ObjectDoesNotExist:
        return "user does not exist"

    while True:
        if mail == user.mail and password == user.password:
            return userid
        elif mail != user.mail or password != user.password:
            return "mail or password are incorrect"

        userid += 1

        try:
            user = User.objects.get(id=userid)
        except ObjectDoesNotExist:
            return "user does not exist"






def profile(request):
    user = User.objects.get(id=2)  # Fetch the user with id 2

    if request.method == 'POST':
        # Extract updated values from the form submission
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        description = request.POST.get('description')

        # Update the user object with the new values
        user.name = name
        user.age = age
        user.email = email
        user.description = description

        # Save the user object to persist the changes in the database
        user.save()

        # Redirect to the profile page
        return redirect('profile')

    # Prepare the initial context for the template
    context = {"mail": user.mail, "name": user.name, "age": user.age, "description": user.description}

    # Render the profile page template with the context
    return render(request, 'profilepage.html', context=context)


def homepage(request):
    return render(request, 'project/homepage.html')

def login_button(request):
    print("hello")
    if request.method == 'POST':  #
        mail = request.POST.get('mail')
        password = request.POST.get('password')
        if type(getIdByUserCredentials(mail,password)) is int:
            return render(request, 'profilepage.html')

# views.py

