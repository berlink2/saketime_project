from django.db import models
from django.shortcuts import reverse
# Create your models here.
from django.utils.text import slugify
from .brewery import Brewery

SAKE_TYPES = (
    ('jd','Junmai Daiginjo'),
('d','Daiginjo'),
('jg','Junmai Ginjo'),
('g', 'Ginjo'),
('j','Junmai'),
('h','Honjozo'),
    ('f','Futsu'),
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


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    short_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=100)
    active = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    date_updated = models.DateTimeField(auto_now=True)
    average_rating = models.FloatField(default=0, null=True,blank=True)
    abv = models.FloatField(default=0)
    tags = models.ManyToManyField(ProductTag, blank=True)
    sake_type = models.CharField(max_length=3, choices=SAKE_TYPES)
    brewery = models.ForeignKey(Brewery, null=True, blank=True, on_delete=models.CASCADE)

    objects = ProductManager()

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







