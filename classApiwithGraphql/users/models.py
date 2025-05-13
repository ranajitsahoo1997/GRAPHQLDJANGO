from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class ExtendUser(AbstractUser):
    
    email = models.CharField(max_length=255,blank=False,verbose_name="email")
    link = models.CharField(max_length=200)
    
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    
class Post(models.Model):
    user = models.ForeignKey(
        ExtendUser,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    


