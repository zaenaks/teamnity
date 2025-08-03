from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Tag

# Create your models here.
User = get_user_model()

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)

    email = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    profile_picture = models.ImageField(upload_to='team_pics/', blank=True, null=True)

    tags = models.ManyToManyField(Tag, blank=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_teams')

    #Налаштування конфіденційності
    is_public = models.BooleanField(default=True)
    is_email_public = models.BooleanField(default=True)

    telegram = models.URLField(blank=True, null=True)
    discord = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class TeamMembership(models.Model):
    ROLES = (
        ('owner', 'Власник'),
        ('member', 'Учасник'),
    )

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_memberships')
    role = models.CharField(max_length=20, choices=ROLES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.team.name} ({self.role})"