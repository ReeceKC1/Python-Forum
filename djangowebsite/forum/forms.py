from django.utils.translation import gettext_lazy as _
from .models import ForumUser, Post, Comment
from django import forms

# Page used for forms used to gather data from Users

# Choices for home page sorting, used in SortForm
SORT_CHOICES = (
    (0, _("Sort")),
    (1, _("Date")),
    (2, _("Rates")),
    (3, _("Title")),
    (4, _("Poster"))
)

# Form for getting profile picture for users, used on Register and Settings page
class ImageForm(forms.Form):
    newimage = forms.ImageField(required=False)

# Form for sort options in site Home page
class SortForm(forms.Form):
    sortchoice = forms.ChoiceField(choices=SORT_CHOICES,initial='0',widget=forms.Select(attrs={'class': 'sortbar', 'onchange': "form.submit();",}))

class ModifyUserForm(forms.ModelForm):
    class Meta:
        model = ForumUser
        fields = [
            'username',
            'password',
            'image'
        ]

# Form used for creation of Post objects, used on Createpost page
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

# Form used for creating of Comment objects, used on Post pages
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]
        widgets = {
            'content': forms.TextInput(
                attrs={
                    'class': 'comment-data',
                }),
       }
