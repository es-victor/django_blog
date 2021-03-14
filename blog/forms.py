from django.forms import ModelForm, Textarea, CheckboxSelectMultiple
from .models import Comment, Post


class NewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={'rows': 3, 'cols': 100, 'class': 'bg-light'}),
        }


class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'categories']
        widgets = {
            'categories': CheckboxSelectMultiple()
        }
