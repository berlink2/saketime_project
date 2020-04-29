from django.db import models
from .userprofile import UserProfile
from .product import Product
from django.contrib.auth import get_user_model
import numpy as np

"""
Represents a Review, written by a User about a Gin

Each user can only write one review about each gin
"""


class Review(models.Model):
    RATING_CHOICES = (
        (1,'1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )


    date = models.DateField('Date published',blank=True, null=True)
    rating = models.IntegerField(choices=RATING_CHOICES, null=True)
    content = models.TextField('Write your review here...')
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews')
    sake = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    postcode = models.CharField(blank=True, null=True, max_length=128)

    class Meta:
        # use a combination of the user and the gin as primary key
        unique_together = ('user', 'sake',)

    def __str__(self):
        return self.user.user.username + ": " + self.sake.name


