from django.db import models
from django.shortcuts import reverse
# Create your models here.
from django.utils.text import slugify
from .brewery import Brewery
import numpy as np

SAKE_TYPES = (
    ('jd','Junmai Daiginjo'),
('d','Daiginjo'),
('jg','Junmai Ginjo'),
('g', 'Ginjo'),
('j','Junmai'),
('h','Honjozo'),
    ('f','Futsu'),
    ('o','Other'),
)


class ProductTagManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class ProductTag(models.Model):
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=48)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    objects = ProductTagManager()

    def natural_key(self):
        return (self.slug,)

    def __str__(self):
        return self.name


class ProductManager(models.Manager):
    def active(self):
        return self.filter(active=True)

    def in_stock(self):
        return self.filter(in_stock=True)

    def get_by_natural_key(self, slug):
        return self.get(slug=slug),



class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True,null=True)
    short_description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    slug = models.SlugField(max_length=100,null=True)
    active = models.BooleanField(default=True,blank=True,null=True)
    in_stock = models.BooleanField(default=True,blank=True,null=True)
    date_updated = models.DateTimeField(auto_now=True,null=True)
    average_rating = models.FloatField(default=0, null=True,blank=True)
    abv = models.FloatField(default=0,blank=True,null=True)
    tags = models.ManyToManyField(ProductTag, blank=True)
    sake_type = models.CharField(max_length=3, choices=SAKE_TYPES)
    brewery = models.ForeignKey(Brewery, null=True, blank=True, on_delete=models.CASCADE, related_name='products')
    volume = models.PositiveIntegerField(blank=True, null=True)
    units_sold = models.PositiveIntegerField(blank=True,null=True,default=0)

    objects = ProductManager()

    def average_rating(self):
        if self.reviews.all():
            all_ratings = map(lambda x:x.rating, self.reviews.all())
            return np.mean(list(all_ratings))
        else:
            return None

    def review_amount(self):
        if self.reviews.all():
            return len([self.reviews.all()])
        else:
            return 0.0

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug':self.slug})

    def natural_key(self):
        return (self.slug,)

    def image_all(self):
        return self.images.all()

    def first_image(self):
        return self.images.first()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    # def get_add_to_cart_url(self):
    #     return reverse('add-to-cart', kwargs={
    #         'slug': self.slug
    #     })




class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product-images')
    #thumbnail = models.ImageField(upload_to='product-thumbnails', null=True)


    def __str__(self):
        return self.product.name









