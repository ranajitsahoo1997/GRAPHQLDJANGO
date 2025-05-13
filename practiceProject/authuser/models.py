from django.db import models

from django.contrib.auth.models import AbstractUser

class AuthUser(AbstractUser):
    """
    Custom user model that extends AbstractUser.
    """
    # Add any additional fields you want to include in your custom user model
    # For example:
    # bio = models.TextField(blank=True)
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    
    email = models.EmailField(unique=True, max_length=255, blank=False,verbose_name='email')
    
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    
    
    def __str__(self):
        return self.username
