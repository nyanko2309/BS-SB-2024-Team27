from django.core.checks import templates
from django.http import HttpResponse
from django.shortcuts import render



def login_view(request):
    return HttpResponse('templates/Login.html')
def homepage(request):
    return render(request, 'project/homepage.html')


# views.py

