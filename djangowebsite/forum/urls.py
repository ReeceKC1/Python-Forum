from django.urls import path
from . import views

urlpatterns = [
    #empty to be default page visited, views.home is the function to use
    path('', views.home, name='forum-home'),
    path('profile/', views.profile, name='forum-profile'),
    path('register/', views.register, name='forum-register'),
]
