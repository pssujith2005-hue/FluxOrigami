from django.db import models
from django.contrib.auth.models import User

class Generation(models.Model):
    """Stores the history of user prompts and AI responses."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generations')
    prompt = models.TextField()
    html_code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class Folder(models.Model):
    """Stores user-created folders for organization."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class Component(models.Model):
    """Stores saved reusable UI components."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_components')
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True, blank=True, related_name='components')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default="UI Component")
    html_code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']