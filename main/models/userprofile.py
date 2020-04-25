from django.contrib.auth import get_user_model
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images', default='profile_images/masu_profile.jpg')

    def __str__(self):
        return self.user.username

