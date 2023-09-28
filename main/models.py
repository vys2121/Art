from distutils.command.upload import upload
from re import T
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.forms import CharField
from embed_video.fields import EmbedVideoField

User= get_user_model()

# Create your models here.
class profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    first_name=models.CharField(max_length=50,blank=True)
    second_name=models.CharField(max_length=50,blank=True)
    bio = models.TextField(max_length=5000,blank=True)
    bgimage = models.ImageField(upload_to='bg_image',default='bg.jpg')
    profileimg = models.ImageField(upload_to='profile_image',default='blank_profile.png')
    location = models.CharField(max_length=100, blank=True)
    Profession=models.CharField(max_length=50, blank=True)
    Relationship=models.CharField(max_length=25,blank=True)

    def _str_(self):
        return self.user.username

class Post(models.Model):
    id= models.UUIDField(primary_key=True,default=uuid.uuid4)
    user= models.CharField(max_length=10)
    image= models.ImageField(upload_to='post_image', blank=True)
    caption=models.TextField(blank=True)
    created_at=models.DateTimeField(default=datetime.now)
    no_of_likes=models.IntegerField(default=0)
    

    def _str_(self):
        return self.user

class LikePost(models.Model):
    post_id=models.CharField(max_length=500)
    username=models.CharField(max_length=100)

    def _str_(self):
        return self.username

class Follower(models.Model):
    Following=models.CharField(max_length=100)
    user=models.CharField(max_length=100)  

    def __str__(self):
        return self.user
    