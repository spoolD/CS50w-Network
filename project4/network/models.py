from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    #following

    #followed by
    
    def __str__(self):
        return self.username

class Posting(models.Model):
    #relationship to User, timestamp, body, users who like
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_by')
    liked = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='likes')
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.TextField(blank=True)
