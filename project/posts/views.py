from django.shortcuts import render, redirect
from .forms import PostForm


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()  # reference the form save as post
            # Set a flag to indicate successful post creation
            post_created = True
            post.save()  # saves the post into the database
            return render(request, 'create_post.html', {'form': form, 'post_created': post_created})
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})
