from django.db import models
from django.utils import timezone
from django import forms

class User(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    image = models.ImageField(blank=True)

#search tags with query tags LIKE %word%
class Post(models.Model):
    id = models.AutoField(max_length=100, primary_key=True)
    poster = models.CharField(max_length=32)
    title = models.CharField(max_length=100)
    image = models.ImageField(blank=True)
    content = models.TextField(blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=0)
    tags = models.CharField(max_length=1000, default='')

    def __str__(self):
        return self.title

class Comment(models.Model):
    id = models.AutoField(max_length=100, primary_key=True)
    poster = models.CharField(max_length=32)
    postid = models.IntegerField()
    content = models.TextField()
    rating = models.IntegerField(default=0)

class Rate(models.Model):
    id = models.AutoField(max_length=100, primary_key=True)
    user = models.CharField(max_length=32)
    contentid = models.IntegerField()
    rate = models.BooleanField()

class Tag(models.Model):
    text = models.TextField(max_length=32, primary_key=True)
