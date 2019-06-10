from django import forms
from .models import ForumUser, Post
from django.utils.translation import gettext_lazy as _

class RegisterForm(forms.ModelForm):
    class Meta:
        model = ForumUser
        fields = [
            'username',
            'password',
            'image',
        ]

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Username',
                    'class': 'register-name',
                }),
            'pasword': forms.PasswordInput(),
            'image': forms.FileInput(
                attrs={
                    'class': 'register-image',
                }),
        }
        labels = {
            'username': 'Writer',
        }

        error_messages = {
        'username': {
            'required': 'Please let us know what to call you!'
        }
        }

class ModifyUserForm(forms.ModelForm):
    class Meta:
        model = ForumUser
        fields = [
            'username',
            'password',
            'image'
        ]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'image',
            'content',
            'tags',
        ]
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Title',
                    'class': 'createpost-title',
                }),
            'content': forms.Textarea(
                attrs={
                    'class': 'createpost-content',
                    'placeholder': 'Content',
                }),
            'tags': forms.Textarea(
                attrs={
                    'class': 'createpost-tags',
                    'placeholder': 'Tags by Space',
                }),
            'image': forms.FileInput(
                attrs={
                    'class': 'createpost-image',
                }),
        }
