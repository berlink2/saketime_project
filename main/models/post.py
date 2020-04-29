from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from main.models import UserProfile

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    lede = models.CharField(max_length=200, blank=True,null=True)
    date = models.DateTimeField(blank=True,null=True)
    image = models.ImageField(upload_to='post-images', blank=True, null=True)
    body = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])