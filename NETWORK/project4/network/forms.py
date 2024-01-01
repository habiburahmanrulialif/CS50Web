from django.forms import ModelForm
from .models import Post, Follow

class PostForm(ModelForm):
    class Meta:
        model : Post
        fields : ["post_image", "post_text"]