from encrypted_model_fields.fields import EncryptedCharField
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models

# Page used for definition of Models used in database

# User model that extends AbstractUser
#   Uses custon username(pk), image(profile picture), and isadmin(tells if user is an admin)
#   Uses default password from AbstractUser, uses make_pasword() to create password and
#   check_password() to test correctness
class ForumUser(AbstractUser):
    username = models.CharField(max_length=32, primary_key=True)
    isadmin = models.BooleanField(default=False)
    #password = EncryptedCharField()
    image = models.ImageField(upload_to='profile_image', default='default.jpg')
    def __str__(self):
        return 'Username:' + self.username + ' IsAdmin:' + str(self.isadmin)

# Post model
#   Uses custom id(pk), poster(ForumUser username), title, image, content(text),
#   date_posted(creation date), rating(number of rate objects), tags(string with key words)
class Post(models.Model):
    id = models.AutoField(max_length=100, primary_key=True)
    poster = models.CharField(max_length=32)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_image',blank=True)
    content = models.TextField(blank=True, default='')
    date_posted = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField()
    tags = models.CharField(max_length=1000, default='')
    def __str__(self):
        return 'ID:' + str(self.id) + ' Title:' + self.title + ' Poster:' + self.poster

# Comment model
#   Uses custom id(pk), poster(ForumUser username), postid(id of post comment is part of),
#   content(text)
class Comment(models.Model):
    id = models.AutoField(max_length=100, primary_key=True)
    poster = models.CharField(max_length=32)
    postid = models.IntegerField()
    content = models.TextField()
    def __str__(self):
        return 'ID:' + str(self.id) + ' Poster:' + self.poster + ' PostID:' + str(self.postid)

# Rate model
#   Uses custom id(pk), user(ForumUser who created rate), contentid(id of post),
#   contentposter(username of creator of post rate was created for), rate(True for uprate/ False for downrate)
class Rate(models.Model):
    id = models.AutoField(max_length=100, primary_key=True)
    user = models.CharField(max_length=32)
    contentid = models.IntegerField(default=0)
    contentposter = models.CharField(max_length=32)
    rate = models.BooleanField()
    def __str__(self):
        return 'ID:' + str(self.id) + ' ContentID:' + str(self.contentid) + ' User:' + self.user
