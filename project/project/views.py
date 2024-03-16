from login.models import User
from django.http import JsonResponse
from posts.models import Post
from django.shortcuts import render, redirect
from login.forms import RegistrationForm


def getIdByUserCredentials(mail_u, password_u) -> int | str:
    try:
        user = User.objects.get(mail=mail_u, password=password_u)
        return user.id
    except User.DoesNotExist:
        return "user does not exist"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "error occurred"


def profile(request):
    global_user_id = request.session.get('global_user_id')
    if global_user_id:
        user = User.objects.get(id=global_user_id)
        context = {'user': user}
        return render(request, 'profilepage.html', context)
    else:
        return redirect('login')


def homepage(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'homepage.html', context)


def login(request):
    return render(request, 'login.html')


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
            #messages.error(request, 'Invalid credentials. Please try again.')
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
            #messages.success(request, 'Registration successful! You can now login.')
            return redirect('login')
        else:
            print("Form is not valid!")
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def register(request):
    return render(request, 'register.html')


def myposts(request):
    return render(request, 'posts.html')


def helppage(request):
    return render(request, 'helppage.html')


def TOS(request):
    return render(request, 'TOS.html')
def create_post(request):
     return render(request, 'create_post.html')