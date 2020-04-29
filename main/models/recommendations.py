from django.db import models
from django.contrib.auth import get_user_model
from .userprofile import UserProfile


class Cluster(models.Model):

    name = models.CharField(max_length=150)
    users = models.ManyToManyField(UserProfile)


    def get_members(self):
        return '\n'.join([user.get_username() for user in self.users.all()])