from django.shortcuts import render
#from django.http import HttpResponse

users = [
    {
        'id': '1',
        'name': 'test_user_1',
        'password': 'password',
        'image': '',
        'likes': ['1','2']
    },
    {
        'id': '2',
        'name': 'test_user_2',
        'password': 'password',
        'image': '',
        'likes': ['3']
    }
]

posts = [
    {
        'id': '1',
        'title': 'test_post_1',
        'content': 'This is test post #1',
        'image': '',
        'poster': '1',
        'rating': 10,
        'date_posted': '100',
        'comments': ['1'],
        'tags': ['test1']
    },
    {
        'id': '2',
        'title': 'test_post_2',
        'content': 'This is test post #2',
        'image': '',
        'poster': '2',
        'rating': -3,
        'date_posted': '200',
        'comments': ['1'],
        'tags': ['test2','feedthedevs']
    },
    {
        'id': '3',
        'title': 'test_post_3',
        'content': '',
        'image': '',
        'poster': '1',
        'rating': 0,
        'date_posted': '300',
        'comments': ['1'],
        'tags': ['test3'],
    }
]

comments = [
    {
        'id': '1',
        'poster': '2',
        'body': 'This is cool!',
        'rating': 10,
    }
]

def home(request):
    #Content to pass in
    content = {
        'users': users,
        'posts': posts,
        'comments': comments
    }
    #displaying a view
    return render(request, 'forum/home.html', content)

def profile(request):
    #display direct HttpResponse
    #return HttpResponse('<h1>Profile</h1>')
    return render(request, 'forum/profile.html')
