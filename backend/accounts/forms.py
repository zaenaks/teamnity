from django import forms
from django.contrib.auth.forms import AuthenticationForm #

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логін", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))