from dataclasses import fields
from django import forms
from .models import Comment
class CommnetForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields = ('comment_text',)