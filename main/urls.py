from distutils.command.upload import upload
from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('index', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('profile1/<str:pk>',views.profile1, name="profile1"),
    path('logout', views.logout, name="logout"),
    path('search', views.search, name="search"),
    path('setting', views.setting, name="setting"),
    path('upload', views.upload, name="upload"),
    path('follow', views.follow, name="follow"),
    path('likepost', views.likepost, name="likepost"),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    
]
