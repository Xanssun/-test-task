from django.contrib import admin
from .models import Like, News, Comment

admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Like)
