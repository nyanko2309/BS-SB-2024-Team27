from django.core.checks import templates
from django.http import HttpResponse
from django.shortcuts import render
from login.models import User
from django.template.loader import get_template, render_to_string


def login(request):
    currentid=0
    user = User.objects.get(id=getidbyuser(m,p) )  # Fetch the user with id 2
    HTML = render_to_string('Login.html', )  # Render the template
    return HttpResponse(HTML)

def profile(request):
    user = User.objects.get(id=getidbyuser(m, p))  # Fetch the user with id 2
    context = {"mail": user.mail, "name": user.name, "age": user.age,
               "description": user.description}  # Pass user.mail to the template context
    HTML = render_to_string('profilepage.html', context=context)  # Render the template
    return HttpResponse(HTML)
def homepage(request):
    return render(request, 'project/homepage.html')


# views.py

