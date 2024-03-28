from login.models import User
from django.http import JsonResponse
from posts.models import Post
from django.shortcuts import render, redirect
from login.forms import RegistrationForm
import json
from django.contrib.auth import logout
from django.shortcuts import redirect
from posts.forms import PostForm
from django.contrib import messages
from django.http import JsonResponse

""" gets id from user after login """


def getIdByUserCredentials(mail_u, password_u) -> int | str:
    try:
        user = User.objects.get(mail=mail_u, password=password_u)
        return user.id
    except User.DoesNotExist:
        return "user does not exist"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "error occurred"


"""adds id to arr"""


def addtoaarr(arr, id):
    if id not in arr:
        arr.append(id)


"""removes id from arr"""


def removefromarr(arr, id):
    if id in arr:
        arr.remove(id)


""" goes to profile,then showing id from db that has user.id """


def profile(request):
    global_user_id = request.session.get('global_user_id')
    context = None
    if global_user_id:
        user = User.objects.get(id=global_user_id)
        context = {'user': user}
    return render(request, 'profilepage.html', context)


"""sends favorites and posts arrs to html homepgae.starts homepage """


def homepage(request):
    posts = Post.objects.all()
    global_user_id = request.session.get('global_user_id')

    if global_user_id:
        user = User.objects.get(id=global_user_id)
        favorites = [int(fav) for fav in user.favorites]
    else:
        favorites = []  # Initialize favorites as an empty list if user is not logged in

    context = {'posts': posts, 'favorites': favorites}
    return render(request, 'homepage.html', context)


"""login page"""


def login_page(request):
    return render(request, 'Login.html')


"""gets stuff from html page,puts it into db"""


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


"""checks if things got from html are in db"""


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


"""if input valid,regiser the user and go to login"""


def submit(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['mail']
            # Check if the email is not allowed
            if is_not_allowed_email(email):
                messages.error(request, 'אימייל זה חסום')
            else:
                user = form.save(commit=False)
                user.mail = email
                user.save()
                messages.success(request, 'ההרשמה בוצעה בהצלחה')
                return redirect('login_page')
        else:
            print("Form is not valid!")
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


"""onclick register button"""


def register(request):
    return render(request, 'register.html')


"""to do fix!!!!!!!!!"""
"""goesto myposts html,"""


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


"""sends 2 arrs,favorites and posts with id of favorites"""


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

        context = {'posts': posts, 'favorites': favorites_ids}
        return render(request, 'homepage.html', context)
    else:
        # Handle case where user is not logged in
        return JsonResponse({'error': 'User not logged in'}, status=401)


"""adds an id to a favorites arr onclick star button """


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


def delete_account(request):
    if request.method == 'POST':
        global_user_id = request.session.get('global_user_id')
        if global_user_id:
            # Retrieve the user object
            user = User.objects.get(id=global_user_id)

            # Delete the user and logout
            user.delete()
            logout(request)
            return redirect('login_page')
        else:
            return JsonResponse({'error': 'User not logged in'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def is_not_allowed_email(email):
    # Define a list of not allowed email addresses
    not_allowed_emails = ['bademail@example.com', '3124@e444.com',
                          'undesirable@example.com']  # Add your not allowed email addresses here

    # Check if the email is in the not allowed list
    if email in not_allowed_emails:
        return True
    else:
        return False


from django.contrib import messages

def create_post_button(request):
    global_user_id = request.session.get('global_user_id')
    user = User.objects.get(id=global_user_id)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            if len(user.my_posts) <= 3:
                saved_post = form.save()
                saved_post_id = saved_post.id
                addtoaarr(user.my_posts, saved_post_id)
                user.save()
                return redirect('myposts')
            else:
                # Display error message
                messages.error(request, 'Too many posts from one user.')
        else:
            # Display form errors
            messages.error(request, 'Form is not valid. Please correct the errors.')
            print(form.errors)
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form, 'errors': messages.get_messages(request)})



def remove_post(request, post_id):
    global_user_id = request.session.get('global_user_id')
    if global_user_id:
        user = User.objects.get(id=global_user_id)
        if post_id in user.my_posts:
            post = Post.objects.get(id=post_id)
            removefromarr(user.my_posts, post_id)
            user.save()
            post.delete()
            messages.success(request, 'Post removed successfully!')
        else:
            messages.error(request, 'Post not found in user\'s posts!')
    else:
        messages.error(request, 'User not logged in!')
    return redirect('myposts')




def rate_site(request):
    if request.method == 'POST':
        rating_value = int(request.POST.get('rating', 0))

        if 0 <= rating_value <= 5:
            # Get the current user
            user = request.user

            # Update the rating for the current user
            user.site_rating = rating_value
            user.save()

            # Calculate average rating
            all_ratings = [u.site_rating for u in User.objects.exclude(site_rating=0)]
            if all_ratings:
                average_rating = sum(all_ratings) / len(all_ratings)
                rating_count = len(all_ratings)
            else:
                average_rating = 0
                rating_count = 0

            # Return success response with updated rating information
            return JsonResponse({'success': True, 'average_rating': average_rating, 'rating_count': rating_count})

        else:
            # Return JSON response with error message
            return JsonResponse({'success': False, 'error': 'Invalid rating value'})

    else:
        # Handle GET request for rendering the rating page
        initial_rating = request.user.site_rating if request.user.is_authenticated else None
        all_ratings = [u.site_rating for u in User.objects.exclude(site_rating=0)]
        if all_ratings:
            average_rating = sum(all_ratings) / len(all_ratings)
            rating_count = len(all_ratings)
        else:
            average_rating = 0
            rating_count = 0

        context = {'initial_rating': initial_rating, 'average_rating': average_rating, 'rating_count': rating_count}
        return render(request, 'rating.html', context)