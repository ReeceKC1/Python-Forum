from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from encrypted_model_fields.fields import EncryptedCharField

class ForumUser(AbstractUser):
    username = models.CharField(max_length=32, primary_key=True)
    #password = EncryptedCharField()
    image = models.ImageField(upload_to='profile_image', default='default.jpg')
    def __str__(self):
        return self.username

#search tags with query tags LIKE %word%
class Post(models.Model):
    id = models.AutoField(max_length=100, primary_key=True)
    poster = models.CharField(max_length=32)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_image',blank=True)
    content = models.TextField(blank=True, default='')
    date_posted = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=0)
    tags = models.CharField(max_length=1000, default='')
    def __str__(self):
        return str(self.id)

class Comment(models.Model):
    id = models.AutoField(max_length=100, primary_key=True)
    poster = models.CharField(max_length=32)
    postid = models.IntegerField()
    content = models.TextField()
    def __str__(self):
        return str(self.id)

class Rate(models.Model):
    id = models.AutoField(max_length=100, primary_key=True)
    user = models.CharField(max_length=32)
    contentid = models.IntegerField()
    rate = models.BooleanField()
    def __str__(self):
        return str(self.id)

class Tag(models.Model):
    text = models.TextField(max_length=32, primary_key=True)
