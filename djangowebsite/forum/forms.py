from django import forms
from .models import User

class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['name', 'password', 'image']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Username'
                }),
            'password': forms.TextInput(
                attrs={
                    'placeholder': 'Password'
                }),
        }
