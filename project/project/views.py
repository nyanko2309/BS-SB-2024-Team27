
from login.models import User
from django.core.exceptions import ObjectDoesNotExist # for helper function
from django.http import JsonResponse
from django.shortcuts import render, redirect

cuser_id=1

def getIdByUserCredentials(mail, password) -> int | str:
    """returns id of a user after receiving mail and password, returns string of 'user doesn't exist' or 'mail or password are incorrect' otherwise"""
    userid = 1

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

#==============================================================
def profile(request):

    # Fetch the user with the specified user_id (assuming User model)
    user = User.objects.get(cuser_id)  # Assuming user ID is fixed for demonstration

    # Prepare the initial context for the template
    context = {"mail": user.mail, "name": user.name, "age": user.age, "description": user.description}

    # Render the profile page template with the context
    return render(request, 'profilepage.html', context=context)

def homepage(request):
    return render(request, 'project/homepage.html')
while(user_id)
    context = {"mail": user.mail, "name": user.name, "age": user.age, "description": user.description}




def login(request):
    return render(request, 'Login.html')
# views.py

# views.py


def save_profile_changes(request):
    if request.method == 'POST':
        # Extract the form data from the POST request
        name = request.POST.get('name')
        age = request.POST.get('age')
        mail = request.POST.get('mail')
        description = request.POST.get('description')

        # Assuming you have a UserProfile model, update the user's profile with the new values
        user_profile = User.objects.get(id=2)  # Assuming user ID is used as profile ID
        user_profile.name = name
        user_profile.age = age
        user_profile.mail = mail
        user_profile.description = description
        user_profile.save()

        # Optionally, you can return a JSON response to indicate success
        return JsonResponse({'message': 'Profile changes saved successfully'})
    else:
        # If the request method is not POST, return an error response
        return JsonResponse({'error': 'Method not allowed'}, status=405)


