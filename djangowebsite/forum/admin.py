from django.contrib import admin
from .models import *

#Register objects to admin
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Rate)
admin.site.register(Tag)
