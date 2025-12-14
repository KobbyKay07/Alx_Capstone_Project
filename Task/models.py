from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username
    
class Tasks(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title