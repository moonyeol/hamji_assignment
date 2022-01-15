from .models import Comment, Choice
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('writer', 'content')


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('choice_text',)
