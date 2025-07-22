from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('signin/', views.LoginUser.as_view(), name='Sign in'),
    path('signup/', views.RegisterUser.as_view(), name='Sign up'),
    path('@<str:username>/', views.UserProfileViews, name='user_profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/edit/', views.UpdateUserView.as_view(), name='profile_edit'),
]