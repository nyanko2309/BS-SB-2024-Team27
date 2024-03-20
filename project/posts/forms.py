from django import forms
from posts.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'location', 'payment', 'work_hours', 'phys_lvl', 'kind_of_job', 'category']
