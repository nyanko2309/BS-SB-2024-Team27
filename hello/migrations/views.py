from django.http import HttpResponse


def logindex(request):
    return HttpResponse("Login.html")