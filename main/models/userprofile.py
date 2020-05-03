from django.contrib.auth import get_user_model
from django.db import models
from cloudinary.models import CloudinaryField


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='userprofile')
    #profile_image = models.ImageField(upload_to='profile_images', default='profile_images/masu_profile.jpg',null=True, blank=True)
    profile_image = CloudinaryField('profile_image')

    def get_username(self):
        return self.user.username

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username

