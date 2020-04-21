# Generated by Django 2.2.12 on 2020-04-21 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('slug', models.SlugField(max_length=100)),
                ('active', models.BooleanField(default=True)),
                ('in_stock', models.BooleanField(default=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('average_rating', models.FloatField(blank=True, default=0, null=True)),
                ('abv', models.FloatField(default=0)),
            ],
        ),
    ]
