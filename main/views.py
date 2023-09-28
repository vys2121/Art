from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
# To protect from urls login 
from django.contrib.auth.decorators import login_required
from numpy import delete
from requests import request
#
import random
from .models import LikePost, Post, profile,Follower
from django.contrib.auth.models import AbstractUser
from itertools import chain
from storages.backends.azure_storage import AzureStorage
import logging
logger = logging.getLogger(__name__)



# Create your views here.
def home(request):
    return render(request,"home page.html")


@login_required(login_url='signin')
def index(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile = profile.objects.filter(user=request.user).first()
    

    user_following_list =[]
    feed=[]

    user_following= Follower.objects.filter(Following=request.user.username)
    length=(len(user_following))
    
    for users in user_following:
        user_following_list.append(users.user)
    for username in user_following_list:
        feed_list = Post.objects.filter(user=username)
        feed.append(feed_list)
    feed_list= list(chain(*feed))

    all_users = User.objects.all()
    user_following_all=[]

    for user in user_following:
        user_list=User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestion= [x for x in list(all_users) if (x not in list(user_following))]
    current_user= User.objects.filter(username=request.user.username)
    final_suggestion= [x for x  in list(new_suggestion) if (x not in list(current_user))]
    random.shuffle(final_suggestion)

    username_profile=[]
    username_profile_list=[]

    for users in final_suggestion:
        username_profile.append(users.id)
    for ids in username_profile:
        profile_list=profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_list)
    suggestion=list(chain(*username_profile_list))
    if length ==0:
        post= Post.objects.all().order_by('created_at')
        return render(request, 'index.html',{'user_profile': user_profile,'posts':post,'suggestion':suggestion[:4]})
    else:
        return render(request, 'index.html',{'user_profile': user_profile,'posts':feed_list,'suggestion':suggestion[:4]})
    

def delete(request, id):
    try:
        post = Post.objects.get(id=id)
        if post.user == request.user.username:
            path = str(post.image)
            azure_storage = AzureStorage()
            azure_storage.delete(path)
            post.delete()

    except Exception as e:
        print(f"Error deleting post: {e}")
        return HttpResponse("An error occurred while deleting the post", status=500)  # Return a 
    
    return redirect('/index')

def update(request,id):
    Posts=Post.objects.get(id=id)
    if(Posts.user==request.user.username):
        return render(request,'Update.html',{'post':Posts})
    return redirect('/index')


def updatepost(request, id):
  if request.method=='POST':
        if request.FILES.get('upload_file')==None:
            caption1=request.POST['caption']
            Posts = Post.objects.get(id=id)
            Posts.caption = caption1
            Posts.save()
        elif request.POST['caption']=="":
            image1=request.FILES.get('upload_file')
            Posts = Post.objects.get(id=id)
            azure_storage = AzureStorage()
            azure_storage.delete(str(Posts.image))
            print("image deleted")
            Posts.image = image1
            Posts.save()
        else:
            caption1=request.POST['caption']
            image1=request.FILES.get('upload_file')
            Posts = Post.objects.get(id=id)
            Posts.caption = caption1
            azure_storage = AzureStorage()
            azure_storage.delete(str(Posts.image))
            print("image deleted")
            Posts.image = image1
            Posts.save()
        return redirect('/index')


def signup(request):


    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password= request.POST['password']
        password2= request.POST['password2']

        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')

            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log in user redirect to setting page
                user_login=auth.authenticate(username=username, password=password)
                auth.login(request,user_login)
                #Create profile object for the user
                user_model=User.objects.get(username=username)
                new_profile= profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('setting')
                


            
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')

        

    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        
        user=auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/index')
        else:
            messages.info(request, 'Invalid Credentials')
            return render(request,'signin.html')
            


    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def setting(request):
        user_profile = profile.objects.filter(user=request.user).first()
        if request.method == 'POST':
            if request.FILES.get('image')==None:
                first_name=request.POST['first_name']
                last_name=request.POST['last_name']
                bio=request.POST['bio']
                if request.FILES.get('bg_image')==None:
                    bgimage=user_profile.bgimage
                else:
                    bgimage=request.FILES.get('bg_image')

                image=user_profile.profileimg
                location=request.POST['location']
                Profession=request.POST['Working at']
                

                user_profile.first_name= first_name
                user_profile.second_name= last_name
                user_profile.bio=bio
                user_profile.bgimage=bgimage
                user_profile.profileimg = image
                user_profile.location= location
                user_profile.Profession=Profession
                
                user_profile.save()


    
            if request.FILES.get('image') !=None:
                first_name=request.POST['first_name']
                last_name=request.POST['last_name']
                bio=request.POST['bio']
                if request.FILES.get('bg_image')==None:
                    bgimage=user_profile.bgimage
                else:
                    bgimage=request.FILES.get('bg_image')
                image=request.FILES.get('image')
                location=request.POST['location']
                Profession=request.POST['Working at']
                

                user_profile.first_name= first_name
                user_profile.second_name= last_name
                user_profile.bio= bio
                user_profile.bgimage=bgimage
                user_profile.profileimg = image
                user_profile.location= location
                user_profile.Profession=Profession
                
                user_profile.save()


        return render(request,'setting.html',{'user_profile': user_profile})

@login_required(login_url='signin')
def upload(request):
    if request.method=='POST':
        user= request.user.username
        image=request.FILES.get('upload_file')
        caption=request.POST['caption']
        

        new_post=Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
    else:
        return redirect('/index')
    return redirect('/index')

@login_required(login_url='signin')
def likepost(request):
    username = request.user.username
    post_id=request.GET.get('post_id')
    post=Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    print(like_filter)
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_of_likes= post.no_of_likes+1
        post.save()
        return redirect("/index")

    else:
        like_filter.delete()
        post.no_of_likes= post.no_of_likes-1
        post.save()
        return redirect("/index")
        
@login_required(login_url='signin')    
def profile1(request,pk):
    user_object=User.objects.get(username=pk)
    user_profile=profile.objects.get(user=user_object)
    user_post=Post.objects.filter(user=pk)
    user_post_len=len(user_post)
    follower=request.user.username
    user=pk

    if Follower.objects.filter(Following=follower,user=user).first():
        Text="Unfollow"
    else:
        Text="Follow"
    user_follower=len(Follower.objects.filter(user=pk))
    user_following=len(Follower.objects.filter(Following=pk))



    caption={'user_object':user_object,
    'user_profile':user_profile,
    'user_post':user_post,
    'user_post_len':user_post_len,
    'Text':Text,
    'user_following':user_following,
    'user_follower':user_follower}

    return render(request,'profile.html',caption)

@login_required(login_url='signin')
def follow(request):
    
    if request.method == 'POST':
        follower= request.POST['follower']
        user= request.POST['user']

        if Follower.objects.filter(Following=follower,user=user).first():
            delete_follower=Follower.objects.filter(Following=follower,user=user).first()
            delete_follower.delete()
            return redirect('/profile1/'+user)
        else:
            new_follower=Follower.objects.create(Following=follower,user=user)
            new_follower.save()
            return redirect('/profile1/'+user)

    else:
        return redirect('/index')

@login_required(login_url='signin')
def search(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=profile.objects.get(user=user_object)
    username_profile=[]
    username_profile_list=[]
    
    if request.method == 'POST':
        username =request.POST['username']
        username_obeject=User.objects.filter(username__icontains=username)
       

        for users in username_obeject:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_list=profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_list)

        username_profile_list=list(chain(*username_profile_list))
        print(username_profile_list)
    return render(request,'search.html',{'user_profile':user_profile,'username_profile_list':username_profile_list})
