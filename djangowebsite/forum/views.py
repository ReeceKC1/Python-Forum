from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.views.generic import DetailView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
#from django.http import HttpResponse

#Homepage with posts and filter bar
def home(request):
    if request.method == 'POST':
        filter = request.POST.get('filter',None)
        if filter != '' and filter != ' ':
            posts = Post.objects.filter(tags__contains=filter)

    else:
        posts = Post.objects.all()
    #Content to pass in
    content = {
        'users': ForumUser.objects.all().count(),
        'posts': posts,
        'comments': Comment.objects.all(),
        'tags': Tag.objects.all(),
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
        'rated': posts,
    }
    #Displaying page
    return render(request, 'forum/profile.html', content)

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
        post.tags = post.tags + ' ' + post.poster
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

    content = {'content':'yo'}

    if request.method == 'POST':
        oldpassword = request.POST.get('old-password',None)
        newpassword = request.POST.get('new-password',None)
        newimage = request.POST.get('new-image',request.FILES)
        content = {'content': newimage}



    return render(request, 'forum/settings.html',content)
