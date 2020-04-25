from django.db import models
from django.utils.text import slugify


class Brewery(models.Model):
    name = models.CharField(max_length=250, unique=True, blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='breweries', blank=True)
    lat = models.FloatField(blank=True)
    long = models.FloatField(blank=True)

    class Meta:
        verbose_name_plural = 'Breweries'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brewery, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


