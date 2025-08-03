from django import forms
from .models import Team
from accounts.models import Tag

class TeamForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={'id': 'multiSelect', 'class': 'form-select'}),
        label="Теги",
        required = False
    )

    class Meta:
        model = Team
        fields = [
            'name', 'email', 'location', 'description', 'profile_picture',
            'tags', 'is_public', 'is_email_public',
            'telegram', 'discord', 'instagram', 'github', 'linkedin',
        ]
        labels = {
            'name': 'Назва команди',
            'email': 'Адреса електронної пошти',
            'location': 'Місто і країна',
            'description': 'Опис',
            'profile_picture': 'Зображення команди',
            'is_public': 'Зробити команду видимою для інших',
            'is_email_public': 'Зробити пошту команди видимою для інших',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_email_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'telegram': forms.URLInput(attrs={'class': 'form-control mb-2'}),
            'discord': forms.URLInput(attrs={'class': 'form-control mb-2'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control mb-2'}),
            'github': forms.URLInput(attrs={'class': 'form-control mb-2'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control mb-2'}),
        }