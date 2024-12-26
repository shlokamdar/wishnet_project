from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    pseudoname = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    # Adjusted related_name here
    groups = models.ManyToManyField('groups.Group', related_name='user_groups') 
    def __str__(self):
        return self.username
