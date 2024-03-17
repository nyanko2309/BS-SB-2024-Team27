from django.shortcuts import render, redirect
from .forms import PostForm


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Save the form data without committing to the database yet
            # Set a flag to indicate successful post creation
            post_created = True
            post.save()  # Commit the post to the database
            print("Post saved successfully:", post)  # Debugging statement
            return render(request, 'create_post.html', {'form': form, 'post_created': post_created})
        else:
            print("Form errors:", form.errors)  # Debugging statement for form errors
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})
