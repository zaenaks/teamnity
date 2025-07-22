from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True) #unique=True - забезпечує унікальність

    def __str__(self):
        return self.name
        

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Зв'язок "один до одного" з вбудованим користувачем, щоб додати до нього додаткові дані про профіль

    full_name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True) # Якщо blank=True значить поле не обов'язкове для заповнення
    description = models.TextField(blank=True, null=True)

    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    tags = models.ManyToManyField(Tag, blank=True)

    telegram = models.URLField(blank=True, null=True)
    discord = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    # Визначення відображення об'єкту UserProfile в адмін-панелі
    def __str__(self):
        return self.user.username
    