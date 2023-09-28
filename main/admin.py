import imp
from django.contrib import admin
from .models import profile,Post,LikePost,Follower
# Register your models here.
admin.site.register(profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Follower)
