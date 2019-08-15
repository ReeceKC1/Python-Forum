from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    #empty to be default page visited, views.home is the function to use
    path('', views.home, name='forum-home'),
    path('profile/', views.profile, name='forum-profile'),
    path('register/', views.register, name='forum-register'),
    path('createPost/', views.createPost, name='forum-createpost'),
    path('post/<pk>/', views.postview, name='forum-post'),
    path('login/',auth_views.LoginView.as_view(template_name='forum/login.html') , name='forum-login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='forum/logout.html') , name='forum-logout'),
    path('settings/', views.settings, name='forum-settings'),
    # path(r'^favicon\.ico$',RedirectView.as_view(url='/static/forum/icon.jpg')),
    path('otherprofile/<pk>/', views.otherprofile, name='forum-otherprofile'),
    path('dorate/<int:content_id>/<int:rating>/', views.dorate, name='forum-dorate')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
