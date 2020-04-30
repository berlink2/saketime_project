from django.contrib.auth import get_user_model
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='userprofile')
    profile_image = models.ImageField(upload_to='profile_images', default='staticfiles/images/profile_images/masu_profile.jpg',null=True, blank=True)


    def get_username(self):
        return self.user.username

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username

