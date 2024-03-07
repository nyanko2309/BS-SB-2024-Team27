from login.models import User
from posts.models import Post
from django.core.exceptions import ObjectDoesNotExist  # for helper function
from django.http import JsonResponse
from django.shortcuts import render, redirect

global global_user_id  # Global variable declaration should be avoided make it global maybe

def getIdByUserCredentials(mail_u, password_u) -> int | str:
    try:
        user = User.objects.get(mail=mail_u, password=password_u)
        return user.id
    except User.DoesNotExist:
        return "user does not exist"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "error occurred"

# The profile view function seems correctly indented
def profile(request):
    user = User.objects.get(id=global_user_id)
    context = {'user': user}
    return render(request, 'profilepage.html', context)

# The homepage view function seems correctly indented
from django.shortcuts import render
from posts.models import Post  # Import the Post model


def homepage(request):
    # Retrieve all posts from the database
    posts = Post.objects.all()

    # Pass the retrieved posts to the template
    context = {'posts': posts}

    # Render the homepage template with the posts
    return render(request, 'homepage.html', context)

# The login function seems correctly indented
def login(request):
    return render(request, 'Login.html')

# The save_profile_changes function seems correctly indented
def save_profile_changes(request):
    if request.method == 'POST':
        # Extract the form data from the POST request
        name = request.POST.get('name')
        age = request.POST.get('age')
        mail = request.POST.get('mail')
        description = request.POST.get('description')

        # Assuming you have a UserProfile model, update the user's profile with the new values
        user_profile = User.objects.get(id=global_user_id)  # Assuming user ID is used as profile ID
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

# The login_button function seems correctly indented
def login_button(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')
        password = request.POST.get('password')
        user_id = getIdByUserCredentials(mail, password)

        if isinstance(user_id, int):
            print("YOU LITTLE FUCKER")
            global_user_id = user_id
            # Successful login, redirect to homepage or any desired page
            return render(request, 'homepage.html')
        else:
            # Handle unsuccessful login (e.g., display an error message)
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})

    # If the request method is not POST, render the login form
    return render(request, 'login.html')
