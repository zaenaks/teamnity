from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView

from .forms import LoginUserForm, RegisterUserForm, UserProfileEditForm
from .models import UserProfile

User = get_user_model()


# Create your views here.
def start(request):
    return render(request, 'Start.html')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'Sign in.html'

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'username': self.request.user.username})
    

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'Sign up.html'
    extra_context = {'title': "Створити аккаунт"}

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'username': self.object.username})



def UserProfileViews(request, username):
    profile_user = get_object_or_404(User, username=username)
    try:
        user_profile = UserProfile.objects.get(user=profile_user)
    except UserProfile.DoesNotExist:
        user_profile = None
    # Чи є користувач що зробив запит власником профілю
    is_owner = request.user.is_authenticated and request.user == profile_user

    has_social_links = False
    if user_profile:
        if user_profile.telegram or user_profile.discord or user_profile.instagram or user_profile.github or user_profile.linkedin:
            has_social_links = True
            
    context = {
        'profile_user': profile_user,
        'user_profile': user_profile,
        'is_owner': is_owner,
        'has_social_links': has_social_links,
    }
    return render(request, 'Profile.html', context)


class UpdateUserView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileEditForm
    template_name = 'Profile editing.html'

    def get_object(self, queryset=None):
        user_profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        # created - True якщо об'єкт user_profile щойно був створений, False - якщо об'єкт вже існував і просто був отриманий
        return user_profile
    
    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'username': self.object.user.username})