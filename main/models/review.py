from django.db import models
from .userprofile import UserProfile
from .product import Product
import numpy as np

"""
Represents a Review, written by a User about a Gin

Each user can only write one review about each gin
"""


class Review(models.Model):
    date = models.DateField(blank=True, null=True)
    rating = models.PositiveSmallIntegerField(blank=True, null=True)
    content = models.TextField(blank=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews')
    sake = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    postcode = models.CharField(blank=True, null=True, max_length=128)

    class Meta:
        # use a combination of the user and the gin as primary key
        unique_together = ('user', 'sake',)

    def __str__(self):
        return self.user.user.name + ": " + self.sake.name


