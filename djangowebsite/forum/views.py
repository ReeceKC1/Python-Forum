from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.views.generic import DetailView
from django.contrib.auth.hashers import make_password
#from django.http import HttpResponse

#Homepage with posts and filter bar
def home(request):
    #Content to pass in
    content = {
        'users': ForumUser.objects.all(),
        'posts': Post.objects.all(),
        'comments': Comment.objects.all(),
        'tags': Tag.objects.all()
    }
    #displaying a view
    return render(request, 'forum/home.html', content)

#Profile page with uses infor and rated posts
def profile(request):
    #Checking if user is logged in
    if not request.user.is_authenticated:
        return register(request)
    #Getting liked posts
    posts = [
        Post.objects.get(id=obj.contentid)
        for obj in
        Rate.objects.filter(user=request.user.username, rate=True)
    ]
    content = {
        'profileuser': ForumUser.objects.get(username=request.user.username),
        'rated': posts,
    }
    #Displaying page
    return render(request, 'forum/profile.html', content)

#post page for post created by users
class PostView(DetailView):
    model = Post
    template_name = 'forum/post.html'

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
        return register(request)
    #Creating form
    form = PostForm(request.POST, request.FILES)
    #Checking validation of forms contents
    if form.is_valid():
        post = form.save(commit=False)
        post.poster = request.user.username
        post.save()
        return redirect('forum-home')
    #Creating fresh form if not valid
    else:
        form = PostForm()
    #Displaying page
    return render(request, 'forum/createPost.html', {'form': form})
