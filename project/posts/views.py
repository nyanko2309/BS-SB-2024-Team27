from django.shortcuts import render, redirect
from .forms import PostForm


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Create a new Post object but do not save it yet
            new_post = form.save(commit=False)
            # Assign the current user as the creator of the post
            new_post.creator = request.user
            # Save the post with the creator assigned
            new_post.save()
            return redirect('success_url')  # Redirect to a success URL
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})
