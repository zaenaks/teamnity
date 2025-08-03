from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import UserProfile, Tag


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(max_length=150, label="Логін", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterUserForm(UserCreationForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Підтвердження пароля", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Логін',
            'email': 'Пошта',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Користувач з таким email вже існує.")
        return email
    

class UserProfileEditForm(forms.ModelForm):
    full_name = forms.CharField(label="Ім'я", max_length=100, required=False, 
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(label="Місто і країна", max_length=100, required=False, 
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label="Опис", required=False, 
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))

    tags = forms.ModelMultipleChoiceField(
        queryset = Tag.objects.all(),
        widget = forms.SelectMultiple(attrs={'class': 'form-select'}),
        label = "Теги",
        required = False
    )

    telegram = forms.URLField(label="Telegram", required=False, 
                              widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': "https://t.me/ваше_ім'я"}))
    discord = forms.URLField(label="Discord", required=False, 
                             widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': "https://discordapp.com/users/вашID"}))
    instagram = forms.URLField(label="Instagram", required=False, 
                               widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': "https://instagram.com/ваше_ім'я"}))
    github = forms.URLField(label="GitHub", required=False, 
                            widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': "https://github.com/ваше_ім'я"}))
    linkedin = forms.URLField(label="LinkedIn", required=False, 
                              widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': "https://linkedin.com/ваше_ім'я"}))

    profile_picture = forms.ImageField(label="Зображення профілю", required=False, 
                                        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = UserProfile
        fields = ['full_name', 'location', 'description', 'profile_picture', 'tags',
                  'telegram', 'discord', 'instagram', 'github', 'linkedin']
