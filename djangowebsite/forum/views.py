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
from  django.contrib.auth.hashers import check_password
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db.models import Q


# Logging
logger = logging.getLogger(__name__)


# Homepage with posts and filter bar
def home(request):
    if request.method == 'POST':
        # Filtering posts
        filter = request.POST.get('filter',None)
        form = SortForm(request.POST,request.FILES)
        if filter != '' and filter != ' ':
            posts = Post.objects.filter(tags__contains=filter)
        else:
            posts = Post.objects.all()
        if form.is_valid():
            # Sorting posts by selected
            sortdropdown = form.cleaned_data['sortchoice']
            if not sortdropdown == '0':
                posts = list(posts)
                if sortdropdown == '1':
                    posts.sort(key=lambda x: x.date_posted)
                elif sortdropdown == '2':
                    posts.sort(key=lambda x: x.rating, reverse=True)
                elif sortdropdown == '3':
                    posts.sort(key=lambda x: x.title)
                elif sortdropdown == '4':
                    posts.sort(key=lambda x: x.poster)
        form = SortForm()
    else:
        posts = Post.objects.all()
        form = SortForm()
    # Getting users and total rating
    users = [
        (obj, Rate.objects.filter(contentposter=obj.username,rate=True).count() - Rate.objects.filter(contentposter=obj.username,rate=False).count())
        for obj in
        ForumUser.objects.all()
        ]
    users.sort(key = lambda x: x[1], reverse=True)
    #Content to pass in
    content = {
        'users': users,
        'posts': posts,
        'totalusers': ForumUser.objects.count(),
        'totalposts': Post.objects.count(),
        'form': form,
    }
    #displaying a view
    return render(request, 'forum/home.html', content)

# Function view for administrative roles on objects
def admin(request):
    if not request.user.is_authenticated or request.user.isadmin == False:
        return render(request,'forum/notadmin.html')

    logger.debug(request.user.username + ' accessed the admin page')

    if request.method == 'POST':
        adminfilter = request.POST.get('adminfilter', None)
        userfilter = request.POST.get('userfilter', None)
        postfilter = request.POST.get('postfilter', None)
        commentfilter = request.POST.get('commentfilter', None)
        # Checking filters
        if userfilter or adminfilter:
            users = ForumUser.objects.filter(Q(username__contains=userfilter) | Q(username__contains=adminfilter))
        else:
            users = ForumUser.objects.all()
        if postfilter or adminfilter:
            posts = list(Post.objects.filter(Q(title__contains=postfilter) | Q(title__contains=adminfilter) | Q(id__contains=postfilter) | Q(id__contains=adminfilter) | Q(date_posted__contains=postfilter) | Q(date_posted__contains=adminfilter) | Q(poster__contains=postfilter) | Q(poster__contains=adminfilter) | Q(tags__contains=postfilter) | Q(tags__contains=adminfilter) | Q(content__contains=postfilter) | Q(content__contains=adminfilter)))
        else:
            posts = Post.objects.all()
        if commentfilter or adminfilter:
            comments = list(Comment.objects.filter(Q(id__contains=commentfilter) | Q(id__contains=adminfilter) | Q(poster__contains=commentfilter) | Q(poster__contains=adminfilter) | Q(postid__contains=commentfilter) | Q(postid__contains=adminfilter) | Q(content__contains=commentfilter) | Q(content__contains=adminfilter)))
        else:
            comments = Comment.objects.all()
    else:
        users = ForumUser.objects.all()
        posts = Post.objects.all()
        comments = Comment.objects.all()
    content = {
        'users': users,
        'posts': posts,
        'comments': comments,
    }
    return render(request, 'forum/admin.html', content)

# Profile page with uses infor and rated posts
def profile(request):
    # Checking if user is logged in
    if not request.user.is_authenticated:
        return redirect('forum-login')
    # Getting liked posts
    posts = [
        Post.objects.get(id=obj.contentid)
        for obj in
        Rate.objects.filter(user=request.user.username, rate=True).exclude(contentposter=request.user.username)
    ]
    content = {
        'profileuser': ForumUser.objects.get(username=request.user.username),
        'rated': posts + list(Post.objects.filter(poster=request.user.username)),
    }
    # Displaying pag e
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

# Post detail page with comments and a form to add comments
def postview(request, pk):
    form = CommentForm(request.POST)
    post = Post.objects.get(id=pk)
    # If post request creating the comment object
    if form.is_valid() and request.user.is_authenticated:
        comment = form.save(commit=False)
        comment.poster = request.user.username
        comment.postid = pk
        comment.save()
        logger.debug('Comment with ID: ' + str(comment.id) + ' created')

    form = CommentForm()

    content = {
        # Form for comment submision
        'form': form,
        # Data to be displayed on page
        'post': post,
        'userimage': ForumUser.objects.get(username=post.poster).image,
        # Getting the comment objects and immages of those users
        'comments': reversed([
            (obj, ForumUser.objects.get(username=obj.poster).image)
            for obj in Comment.objects.filter(postid=pk)
        ]),
        'commentcount': Comment.objects.filter(postid=pk).count(),
    }
    return render(request, 'forum/post.html', content)

# Function view for logging in users
def loginuser(request):
    content = {
        'error': None,
    }

    if request.method == 'POST':
        loginusername = request.POST.get('login-username')
        loginpassword = request.POST.get('login-password')
        # Checking username existance and sending error if DNE
        if not ForumUser.objects.filter(username=loginusername):
            content = {
                'error': 'This username does not exist'
            }
            return render(request, 'forum/login.html', content)
        tempuser = ForumUser.objects.get(username=loginusername)
        # Checking users password
        if not check_password(loginpassword,tempuser.password):
            content = {
                'error': 'Incorrect password'
            }
            return render(request, 'forum/login.html', content)
        login(request, tempuser)
        logger.debug('User ' + tempuser.username + ' logged in')
        return profile(request)

    return render(request, 'forum/login.html', content)

# Register page where users can create accounts
def register(request):

    form = ImageForm(request.POST,request.FILES)

    if request.method == 'POST':
        if form.is_valid():
            registerimage = form.cleaned_data['newimage']
            registerusername = request.POST.get('register-username',None)
            registerpassword = request.POST.get('register-password',None)
            registerpaswordconf = request.POST.get('register-password-conf',None)

            # Checking username correctness
            if len(registerusername) > 32 or "/" in registerusername:
                content = {'error': 'Invalid username, must be l32 characters or less and  not contain the \'/\' character'}
                return render(request, 'forum/register.html', content)
            # Checking username availability
            elif ForumUser.objects.filter(username=registerusername):
                content = {'error': 'Username already exists'}
                return render(request, 'forum/register.html', content)
            # Checking if new passwords match
            if not registerpassword == registerpaswordconf:
                content = {'error': 'Passwords do not match'}
                return render(request, 'forum/register.html', content)
            if registerimage:
                registeruser = ForumUser(username=registerusername, password=make_password(registerpassword), image=registerimage)
            else:
                registeruser = ForumUser(username=registerusername, password=make_password(registerpassword))
            registeruser.save()
            logger.debug('User ' + registeruser.username + ' created')
            login(request, registeruser)
            return profile(request)

    content = {
        'error': None,
        'form': ImageForm(),
    }

    return render(request, 'forum/register.html', content)

# Post creation page where users can create posts
def createPost(request):
    # Checking if user is logged in
    if not request.user.is_authenticated:
        return redirect('forum-login')
    # Creating form
    form = PostForm(request.POST, request.FILES)
    # Checking validation of forms contents
    if form.is_valid():
        post = form.save(commit=False)
        post.poster = request.user.username
        post.tags = post.tags + ' ' + post.poster + ' ' + post.title
        post.rating = 0
        post.save()
        logger.debug('Post created by ' + request.user.username + ' with ID: ' + str(post.id))
        return redirect('forum-home')
    # Creating fresh form if not valid
    else:
        form = PostForm()
    # Displaying page
    return render(request, 'forum/createPost.html', {'form': form})

# Function view for Settings page
def settings(request):
    if not request.user.is_authenticated:
        return redirect('forum-login')

    form = ImageForm(request.POST,request.FILES)

    if request.method == 'POST':
        if form.is_valid():
            newimage = form.cleaned_data['newimage']
            oldpassword = request.POST.get('old-password',None)
            newpassword = request.POST.get('new-password',None)
            newpasswordconf = request.POST.get('new-password-conf',None)
            tempuser = ForumUser.objects.get(username=request.user.username)
            # Checking users current password
            if not check_password(oldpassword,ForumUser.objects.get(username=request.user.username).password):
                content = {'error': 'Password is incorrect'}
                return render(request, 'forum/settings.html',content)
            # Checking is new passwords match
            if newpassword and newpasswordconf:
                if not newpassword == newpasswordconf:
                    content = {'error': 'New passwords do not match'}
                    return render(request, 'forum/settings.html',content)
                tempuser.password = make_password(newpassword)
            if newimage:
                tempuser.image = newimage
            tempuser.save()
            logger.debug('Settings changed for user ' + request.user.username)
            login(request,tempuser)
            return redirect('forum-profile')

    content = {
        'error': None,
        'form': ImageForm(),
        }

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

# Function url to rate a post
def dorate(request, content_id, rating):
    # Valid user check
    if request.user.is_authenticated:
        # Duplicate rate check
        if not Rate.objects.filter(user=request.user.username, contentid=content_id, rate=rating):
            logger.debug('Rate created for post ID: ' + str(content_id) + ' with rating ' + str(rating))
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

# Function url to promote/demote user
def promoteuser(request, username):
    if request.user.is_authenticated and request.user.isadmin == True:
        tempuser = ForumUser.objects.get(username=username)
        if tempuser.isadmin == True:
            logger.debug('User ' + username + ' demoted')
        else:
            logger.debug('User ' + username + ' promoted')
        tempuser.isadmin = not tempuser.isadmin
        tempuser.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Function url to remove a user and their posts/comments/rates
def removeuser(request, username):
    if request.user.is_authenticated and request.user.isadmin == True:
        for obj in Comment.objects.filter(poster=username):
            logger.debug('Comment with ID: ' + str(obj.id) + ' deleted')
            Comment.objects.filter(id=obj.id).delete()
        # Deleting rates and decrementing all post ratings associated
        for rate in Rate.objects.filter(Q(user=username) | Q(contentposter=username)):
            if rate.rate == True:
                Post.objects.filter(id=rate.contentid).update(rating=F('rating')-1)
            if rate.rate == False:
                Post.objects.filter(id=rate.contentid).update(rating=F('rating')+1)
            logger.debug('Rate with ID: ' + str(rate.id) + ' deleted')
            Rate.objects.filter(id=rate.id).delete()
        # Deleting posts and all objects related to post
        for obj in Post.objects.filter(poster=username):
            for object in Comment.objects.filter(postid=obj.id):
                logger.debug('Comment with ID: ' + str(object.id) + ' deleted')
                Comment.objects.filter(id=object.id).delete()
            for rate in Rate.objects.filter(contentid=obj.id):
                if rate.rate == True:
                    Post.objects.filter(id=rate.contentid).update(rating=F('rating')-1)
                if rate.rate == False:
                    Post.objects.filter(id=rate.contentid).update(rating=F('rating')+1)
                logger.debug('Rate with ID: ' + str(rate.id) + ' deleted')
                Rate.objects.filter(id=rate.id).delete()
            Post.objects.filter(id=obj.id).delete()
        ForumUser.objects.filter(username=username).delete()
        logger.debug('User with ID: ' + username + ' deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Function url to remove a post and its rates/comments
def removepost(request, postid):
    if request.user.is_authenticated and request.user.isadmin == True:
        for obj in Comment.objects.filter(postid=postid):
            logger.debug('Comment with ID: ' + str(obj.id) + ' deleted')
            Comment.objects.filter(id=obj.id).delete()

        for rate in Rate.objects.filter(contentid=postid):
            if rate.rate == True:
                Post.objects.filter(id=rate.contentid).update(rating=F('rating')-1)
            if rate.rate == False:
                Post.objects.filter(id=rate.contentid).update(rating=F('rating')+1)
            logger.debug('Rate with ID: ' + str(rate.id) + ' deleted')
            Rate.objects.filter(id=rate.id).delete()

        logger.debug('Post with ID: ' + str(postid) + ' deleted')
        Post.objects.filter(id=postid).delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Function url to remove comment object
def removecomment(request, commentid):
    if request.user.is_authenticated and request.user.isadmin == True:
        logger.debug('Comment with ID: ' + str(commentid) + ' deleted')
        Comment.objects.filter(id=commentid).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
