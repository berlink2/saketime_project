# Generated by Django 2.2.12 on 2020-04-25 20:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address1', models.CharField(max_length=60, verbose_name='Address line 1')),
                ('address2', models.CharField(blank=True, max_length=60, verbose_name='Address line 2')),
                ('zip_code', models.CharField(max_length=12, verbose_name='ZIP or Postal code')),
                ('city', models.CharField(max_length=60)),
                ('country', models.CharField(choices=[('uk', 'United Kingdom'), ('us', 'United States of America'), ('jp', 'Japan'), ('id', 'Indonesia')], max_length=3)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='Brewery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, unique=True)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('image', models.ImageField(blank=True, upload_to='breweries')),
                ('lat', models.FloatField(blank=True, null=True)),
                ('long', models.FloatField(blank=True, null=True)),
                ('website', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Breweries',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(10, 'Open'), (20, 'Submitted')], default=10)),
            ],
        ),
        migrations.CreateModel(
            name='CartLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(10, 'New'), (20, 'Paid'), (30, 'Done')], default=10)),
                ('billing_name', models.CharField(max_length=60)),
                ('billing_address1', models.CharField(max_length=60)),
                ('billing_address2', models.CharField(blank=True, max_length=60)),
                ('billing_zip_code', models.CharField(max_length=12)),
                ('billing_city', models.CharField(max_length=60)),
                ('billing_country', models.CharField(max_length=3)),
                ('shipping_name', models.CharField(max_length=60)),
                ('shipping_address1', models.CharField(max_length=60)),
                ('shipping_address2', models.CharField(blank=True, max_length=60)),
                ('shipping_zip_code', models.CharField(max_length=12)),
                ('shipping_city', models.CharField(max_length=60)),
                ('shipping_country', models.CharField(max_length=3)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(10, 'New'), (20, 'Processing'), (30, 'Sent'), (40, 'Cancelled')], default=10)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('short_description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('slug', models.SlugField(max_length=100, null=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('in_stock', models.BooleanField(blank=True, default=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('average_rating', models.FloatField(blank=True, default=0, null=True)),
                ('abv', models.FloatField(blank=True, default=0, null=True)),
                ('sake_type', models.CharField(choices=[('jd', 'Junmai Daiginjo'), ('d', 'Daiginjo'), ('jg', 'Junmai Ginjo'), ('g', 'Ginjo'), ('j', 'Junmai'), ('h', 'Honjozo'), ('f', 'Futsu'), ('o', 'Other')], max_length=3)),
                ('volume', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product-images')),
            ],
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('slug', models.SlugField(max_length=48)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('rating', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('content', models.TextField(blank=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('long', models.FloatField(blank=True, null=True)),
                ('postcode', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(default='profile_images/masu_profile.jpg', upload_to='profile_images')),
            ],
        ),
    ]
