from django.contrib import admin
from .models import *
from .forms import *
from django.contrib.auth.admin import UserAdmin

#Register objects to admin
admin.site.register(ForumUser)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Rate)
admin.site.register(Tag)


class CustomUserAdmin(UserAdmin):
    add_form = RegisterForm
    form = ModifyUserForm
    model = ForumUser
    list_display = ['username',]

admin.site.unregister(ForumUser)
admin.site.register(ForumUser, UserAdmin)
