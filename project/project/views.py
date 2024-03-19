from login.models import User
from django.http import JsonResponse
from posts.models import Post
from django.shortcuts import render, redirect
from login.forms import RegistrationForm
import json


def getIdByUserCredentials(mail_u, password_u) -> int | str:
    try:
        user = User.objects.get(mail=mail_u, password=password_u)
        return user.id
    except User.DoesNotExist:
        return "user does not exist"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "error occurred"


def addtoaarr(arr,id):
    if id not in arr:
        arr.append(id)

def removefromarr(arr,id):
    if id in arr:
        arr.remove(id)

def profile(request):
    global_user_id = request.session.get('global_user_id')
    context=None
    if global_user_id:
        user= User.objects.get(id=global_user_id)
        context = {'user': user}
    return render(request, 'profilepage.html', context)


def homepage(request):
    posts = Post.objects.all()
    global_user_id = request.session.get('global_user_id')

    if global_user_id:
        user = User.objects.get(id=global_user_id)
        favorites = [int(fav) for fav in user.favorites]
        print("Favorites:", favorites)  # Print the favorites list
    else:
        favorites = []  # Initialize favorites as an empty list if user is not logged in
        favorites_str = ""  # Initialize favorites_str as an empty string

    context = {'posts': posts, 'favorites': favorites}
    return render(request, 'homepage.html', context)

def login_page(request):
    return render(request, 'Login.html')


def save_profile_changes(request):
    global_user_id = request.session.get('global_user_id')
    if global_user_id:
        user_profile = User.objects.get(id=global_user_id)

        if request.method == 'POST':
            name = request.POST.get('name')
            age = request.POST.get('age')
            mail = request.POST.get('mail')
            description = request.POST.get('description')

            user_profile.name = name
            user_profile.age = age
            user_profile.mail = mail
            user_profile.description = description
            user_profile.save()

            return JsonResponse({'message': 'Profile changes saved successfully'})
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
    else:
        return JsonResponse({'error': 'User not logged in'}, status=401)


from django.contrib import messages

def login_button(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')
        password = request.POST.get('password')
        user_id = getIdByUserCredentials(mail, password)

        if isinstance(user_id, int):
            request.session['global_user_id'] = user_id
            return redirect('homepage')
        else:
            # Add an error message
            messages.error(request, 'Invalid credentials. Please try again.')
            return render(request, 'login.html')  # Render the login form with the error message
    else:
        return render(request, 'login.html')



def submit(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.mail = form.cleaned_data['mail']
            if User.objects.filter(mail=user.mail).exists():  # Check if email already exists
                messages.error(request, 'Email already exists. Please choose a different email.')
            user.save()
            messages.success(request, 'Registration successful! You can now login.')
            return redirect('login_page')
        else:
            print("Form is not valid!")
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def register(request):
    return render(request, 'register.html')


def myposts(request):

        global_user_id = request.session.get('global_user_id')
        if global_user_id:
            user = User.objects.get(id=global_user_id)
            my_post_ids = user.my_posts  # List of post IDs belonging to the user

            # Filter posts based on user's my_posts list
            posts = Post.objects.filter(id__in=my_post_ids)

            context = {'posts': posts}
            return render(request, 'posts.html', context)
        else:
            # Handle case where user is not logged in
            return JsonResponse({'error': 'User not logged in'}, status=401)


def myfavorites(request):
    global_user_id = request.session.get('global_user_id')
    if global_user_id:
        user = User.objects.get(id=global_user_id)
        favorites_ids = [int(fav) for fav in user.favorites]  # List of post IDs belonging to the user

        # Filter posts based on user's favorites list
        posts = Post.objects.filter(id__in=favorites_ids)

        # Add a boolean field indicating whether each post is in the user's favorites
        for post in posts:
            post.is_favorite = True

        context = {'posts': posts,'favorites': favorites_ids}
        return render(request, 'homepage.html', context)
    else:
        # Handle case where user is not logged in
        return JsonResponse({'error': 'User not logged in'}, status=401)

def add_to_favorites(request):
    if request.method == 'POST':
        global_user_id = request.session.get('global_user_id')
        if global_user_id:
            # Retrieve data from the request body
            data = json.loads(request.body)
            post_id = data.get('postId')

            # Retrieve the user object
            user = User.objects.get(id=global_user_id)

            # Add the post to user's favorites
            if post_id:
                if post_id not in user.favorites:
                    addtoaarr(user.favorites, post_id)
                    user.save()
                    return JsonResponse({'success': True, 'favorites': user.favorites})
                else:
                    removefromarr(user.favorites, post_id)
                    user.save()
                    return JsonResponse({'success': True, 'favorites': user.favorites})
            else:
                return JsonResponse({'error': 'Post ID not provided'}, status=400)
        else:
            # Handle case where user is not logged in
            return JsonResponse({'error': 'User not logged in'}, status=401)


def helppage(request):
    return render(request, 'helppage.html')


def TOS(request):
    return render(request, 'TOS.html')
def create_post(request):
     return render(request, 'create_post.html')
