from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    #empty to be default page visited, views.home is the function to use
    path('', views.home, name='forum-home'),
    path('profile/', views.profile, name='forum-profile'),
    path('register/', views.register, name='forum-register'),
    path('createPost/', views.createPost, name='forum-createpost'),
    path('post/<pk>/', views.PostView.as_view(), name='forum-post'),
    path('login/',auth_views.LoginView.as_view(template_name='forum/login.html') , name='forum-login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='forum/logout.html') , name='forum-logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
