from django.db import models
from django.contrib.auth.models import User # Вбудована модель користувача Django для базової автентифікації


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True) #unique=True - забезпечує унікальність

    def __str__(self):
        return f"#{self.name}"
        

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Зв'язок "один до одного" з вбудованим користувачем, щоб додати до нього додаткові дані про профіль

    nickname = models.CharField(max_length=30)
    full_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True) # Якщо blank=True значить поле не обов'язкове для заповнення
    description = models.TextField(blank=True)

    tags = models.ManyToManyField(Tag, blank=True)

    telegram = models.URLField(blank=True)
    discord = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    # Визначення відображення об'єкту UserProfile в адмін-панелі
    def __str__(self):
        return self.nickname
    