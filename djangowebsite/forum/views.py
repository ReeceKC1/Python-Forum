from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.views.generic import DetailView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import RedirectView
from django.db.models import F
import logging

logger = logging.getLogger(__name__)


#Homepage with posts and filter bar
def home(request):
    if request.method == 'POST':
        filter = request.POST.get('filter',None)
        if filter != '' and filter != ' ':
            posts = Post.objects.filter(tags__contains=filter)
        else:
            posts = Post.objects.all()

    else:
        posts = Post.objects.all()
    users = [
        (obj, Post.objects.filter(poster=obj.username).count())
        for obj in
        ForumUser.objects.all()
        ]
    users.sort(key = lambda x: x[1], reverse=True)
    #Content to pass in
    content = {
        'users': users,
        'posts': posts,
        'comments': Comment.objects.all(),
        'tags': Tag.objects.all(),
        'totalusers': ForumUser.objects.count(),
        'totalposts': Post.objects.count(),
    }
    #displaying a view
    return render(request, 'forum/home.html', content)

#Profile page with uses infor and rated posts
def profile(request):
    #Checking if user is logged in
    if not request.user.is_authenticated:
        return redirect('forum-login')
    #Getting liked posts
    posts = [
        Post.objects.get(id=obj.contentid)
        for obj in
        Rate.objects.filter(user=request.user.username, rate=True)
    ]
    content = {
        'profileuser': ForumUser.objects.get(username=request.user.username),
        'rated': posts + list(Post.objects.filter(poster=request.user.username)),
    }
    #Displaying pag e
    return render(request, 'forum/profile.html', content)

def otherprofile(request, pk):
    try:
        posts = Post.objects.filter(poster=pk)
    except Post.DoesNotExist:
        posts = None

    content = {
        'otheruser': ForumUser.objects.get(username=pk),
        'posts': posts,
    }
    return render(request, 'forum/otherprofile.html', content)

#post detail page with comments and a form to add comments
def postview(request, pk):
    form = CommentForm(request.POST)
    post = Post.objects.get(id=pk)
    #If post request creating the comment object
    if form.is_valid() and request.user.is_authenticated:
        comment = form.save(commit=False)
        comment.poster = request.user.username
        comment.postid = pk
        comment.save()
        form = CommentForm()

    content = {
        #Form for comment submision
        'form': form,
        #Data to be displayed on page
        'post': post,
        'userimage': ForumUser.objects.get(username=post.poster).image,
        #Getting the comment objects and immages of those users
        'comments': reversed([
            (obj, ForumUser.objects.get(username=obj.poster).image)
            for obj in Comment.objects.filter(postid=pk)
        ]),
    }
    return render(request, 'forum/post.html', content)

#register page where users can create accounts
def register(request):
    #Checking if user is logged in
    if request.user.is_authenticated:
        return profile(request)
    #Creating form
    form = RegisterForm(request.POST,request.FILES)
    #Checking validation of forms contents
    if form.is_valid():
        user = form.save(commit=False)
        user.password = make_password(user.password)
        user.save()
        login(request, user)
        return profile(request)
    #Creating fresh form if not valid
    else:
        form = RegisterForm()
    #Displaying page
    return render(request, 'forum/register.html', {'form': form})

#Post creation page where users can create posts
def createPost(request):
    #Checking if user is logged in
    if not request.user.is_authenticated:
        return redirect('forum-login')
    #Creating form
    form = PostForm(request.POST, request.FILES)
    #Checking validation of forms contents
    if form.is_valid():
        post = form.save(commit=False)
        post.poster = request.user.username
        post.tags = post.tags + ' ' + post.poster + ' ' + post.title
        post.rating = 0
        post.save()
        return redirect('forum-home')
    #Creating fresh form if not valid
    else:
        form = PostForm()
    #Displaying page
    return render(request, 'forum/createPost.html', {'form': form})

def settings(request):
    if not request.user.is_authenticated:
        return redirect('forum-login')

    content = None

    if request.method == 'POST':
        oldpassword = make_password(request.POST.get('old-password',None))
        newpassword = request.POST.get('new-password',None)
        newpasswordconf = request.POST.get('new-password-conf',None)
        newimage = request.POST.get('new-image',request.FILES)


        if not oldpassword == ForumUser.objects.get(username=request.user.username).password:
            content = {'error': 'Password is incorrect'}
            return render(request, 'forum/settings.html',content)
        if not newpassword == newpasswordconf:
            content = {'error': 'Passwords do not match'}
            return render(request, 'forum/settings.html',content)

        tempuser = ForumUser.objects.get(username=request.user.username)
        tempuser.password = newpassword
        tempuser.image = newimage
        tempuser.save()


    return render(request, 'forum/settings.html',content)

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import authentication, permissions
# from django.contrib.auth.models import User
#
# class UpRateToggle(APIView):
#     """
#     View to list all users in the system.
#
#     * Requires token authentication.
#     * Only admin users are able to access this view.
#     """
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsUser]
#
#     def get(self, request, format=None):
#         """
#         Return a list of all users.
#         """
#         usernames = [user.username for user in User.objects.all()]
#         return Response(usernames)

# class UpRateRedirect(RedirectView):
#     def get_redirect_url(self, *args, **kwargs):
#         content_id = self.kwargs.get("content_id")
#         rate = self.kwargs.get("rate")
#         if rate == 0:
#             bool = True
#         else:
#             bool = False
#
#         if not Rate.objects.filter(user=request.user.username, contentid=content_id, rate=bool):
#             rating = Rate(user=request.user.username, contentid=content_id, rate=bool)
#             rating.save()
#         return reverse()
def dorate(request, content_id, rating):
    # Valid user check
    if request.user.is_authenticated:
        # Duplicate rate check
        if not Rate.objects.filter(user=request.user.username, contentid=content_id, rate=rating):
            if rating == 1:
                Post.objects.filter(id=content_id).update(rating=F('rating')+1)
            if rating == 0:
                Post.objects.filter(id=content_id).update(rating=F('rating')-1)
            # Creating rate object
            if Rate.objects.filter(user=request.user.username, contentid=content_id, rate=(not rating)):
                Rate.objects.filter(user=request.user.username, contentid=content_id, rate=(not rating)).delete()
                if rating == 1:
                    Post.objects.filter(id=content_id).update(rating=F('rating')+1)
                if rating == 0:
                    Post.objects.filter(id=content_id).update(rating=F('rating')-1)
            Rate.objects.create(user=request.user.username, contentid=content_id, contentposter=Post.objects.get(id=content_id).poster, rate=rating)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
