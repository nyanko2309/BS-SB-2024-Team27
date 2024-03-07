
from login.models import User
from posts.models import Post
from django.core.exceptions import ObjectDoesNotExist # for helper function
from django.http import JsonResponse
from django.shortcuts import render, redirect

global global_user_id

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

#==============================================================
def profile(request):

    # Fetch the user with the specified user_id (assuming User model)
    user = User.objects.get(id=2)  # Assuming user ID is fixed for demonstration

    # Prepare the initial context for the template
    context = {"mail": user.mail, "name": user.name, "age": user.age, "description": user.description}

    # Render the profile page template with the context
    return render(request, 'profilepage.html', context=context)

    # Retrieve all posts from the database

def homepage(request):
  ##posts = Post.objects.all()

#### Pass the posts to the template context
#  context = {
#    'posts': posts
#  }

 # Render the homepage template with the posts
  return render(request, 'project/homepage.html', )


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

def login_button(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')
        password = request.POST.get('password')
        user_id = getIdByUserCredentials(mail, password)
        global_user_id = user_id
        print("EDMUND MCMILLEN")
        if isinstance(user_id, int):
            print("YOU LITTLE FUCKER")
            # Successful login, redirect to homepage or any desired page
            return render(request, 'homepage.html')
        else:
            # Handle unsuccessful login (e.g., display an error message)
            print("YOU MADE A PIECE OF SHIT")
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})

    # If the request method is not POST, render the login form
    return render(request, 'login.html')