from django.db import models
from django.utils.text import slugify


class BreweryManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Brewery(models.Model):
    name = models.CharField(max_length=250, unique=True, blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='breweries', blank=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    website = models.CharField(max_length=100, blank=True)

    objects = BreweryManager()

    class Meta:
        verbose_name_plural = 'Breweries'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brewery, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.slug,)

