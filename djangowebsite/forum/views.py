from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import RegisterForm
#from django.http import HttpResponse

def home(request):
    #Content to pass in
    content = {
        'users': User.objects.all(),
        'posts': Post.objects.all(),
        'comments': Comment.objects.all(),
        'tags': Tag.objects.all()
    }
    #displaying a view
    return render(request, 'forum/home.html', content)

def profile(request):
    #display direct HttpResponse
    #return HttpResponse('<h1>Profile</h1>')
    return render(request, 'forum/profile.html')

def register(request):
    #get display page
    #post add data

    form = RegisterForm(request.POST)

    if form.is_valid():
        user = form.save()
        return redirect('forum-profile')

    return render(request, 'forum/register.html', {'form': form})
