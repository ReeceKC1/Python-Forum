from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

# Page used for url navigation of site

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    # Paths used for views in views.py to display pages on the site
    path('', views.home, name='forum-home'),
    path('admin/', views.admin, name='forum-admin'),
    path('profile/', views.profile, name='forum-profile'),
    path('register/', views.register, name='forum-register'),
    path('createPost/', views.createPost, name='forum-createpost'),
    path('post/<pk>/', views.postview, name='forum-post'),
    path('login/', views.loginuser, name='forum-login'),
    path('settings/', views.settings, name='forum-settings'),
    path('otherprofile/<pk>/', views.otherprofile, name='forum-otherprofile'),
    # Only path not using a function in view.py
    path('logout/', auth_views.LogoutView.as_view(template_name='forum/logout.html') , name='forum-logout'),
    # Paths used for performing tasks
    path('dorate/<int:content_id>/<int:rating>/', views.dorate, name='forum-dorate'),
    path('removeuser/<username>/', views.removeuser, name='forum-removeuser'),
    path('removepost/<int:postid>/', views.removepost, name='forum-removepost'),
    path('removecomment/<int:commentid>/', views.removecomment, name='forum-removecomment'),
    path('promoteuser/<username>/', views.promoteuser, name='forum-promoteuser'),
    # Adding static files to paths
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
