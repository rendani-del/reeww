from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.conf import settings

class User(AbstractUser):
    # Add any additional fields here if needed
    pass

    class Meta:
        # Add this if your app name is 'notes'
        db_table = 'auth_user'  # Optional: maintains same table name as default

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    

    def _str_(self):
        return self.title
# Create your models here.
