from django.db import models
from django.utils import timezone
from encrypted_model_fields.fields import EncryptedCharField

class User(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    password = EncryptedCharField(max_length=100)
    image = models.ImageField(blank=True, default='')
    def __str__(self):
        return self.name

#search tags with query tags LIKE %word%
class Post(models.Model):
    id = models.AutoField(max_length=100, primary_key=True)
    poster = models.CharField(max_length=32)
    title = models.CharField(max_length=100)
    image = models.ImageField(blank=True, default='')
    content = models.TextField(blank=True, default='')
    date_posted = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=0)
    tags = models.CharField(max_length=1000, default='')
    def __str__(self):
        return self.id

class Comment(models.Model):
    id = models.AutoField(max_length=100, primary_key=True)
    poster = models.CharField(max_length=32)
    postid = models.IntegerField()
    content = models.TextField()
    def __str__(self):
        return self.id

class Rate(models.Model):
    id = models.AutoField(max_length=100, primary_key=True)
    user = models.CharField(max_length=32)
    contentid = models.IntegerField()
    rate = models.BooleanField()
    def __str__(self):
        return self.id

class Tag(models.Model):
    text = models.TextField(max_length=32, primary_key=True)
