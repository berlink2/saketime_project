from django.contrib.auth import get_user_model
from django.db import models


class UserProfile(models.Model):
    #userprofile = get_user_model()
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='userprofile')
    #username = models.CharField(userprofile.username, blank=True, null=True, max)
    profile_image = models.ImageField(upload_to='profile_images', default='static/profile_images/masu_profile.jpg',null=True, blank=True)
    #email = models.EmailField(userprofile.email, blank=True, null=True)
    #Phone = models.IntegerField(blank=True, null=True)

    def get_username(self):
        return self.user.username

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username

