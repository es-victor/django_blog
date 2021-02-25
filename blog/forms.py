from django.forms import ModelForm, Textarea
from .models import Comment


class NewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={'rows': 3, 'cols': 100, 'class': 'bg-light'}),
        }
