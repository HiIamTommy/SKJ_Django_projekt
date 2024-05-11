from django.contrib import admin
from .models import AppUser, Post, Comment, Following, SportEvent, SportCategory, Notification

# Register your models here.
admin.site.register(AppUser)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Following)
admin.site.register(SportEvent)
admin.site.register(SportCategory)
admin.site.register(Notification)

