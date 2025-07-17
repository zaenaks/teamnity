from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .forms import LoginUserForm
from .models import UserProfile

# Create your views here.
def start(request):
    return render(request, 'Start.html')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'Sign in.html'

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'username': self.request.user.username})

def SignUp(request):
    return render(request, 'Sign up.html')

def UserProfileViews(request, username):
    profile_user = get_object_or_404(User, username=username)

    try:
        user_profile = UserProfile.objects.get(user=profile_user)
    except UserProfile.DoesNotExist:
        user_profile = None

    is_owner = request.user.is_authenticated and request.user == profile_user

    context = {
        'profile_user': profile_user,
        'user_profile': user_profile,
        'is_owner': is_owner,
    }
    return render(request, 'Profile.html', context)