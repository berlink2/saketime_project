# Generated by Django 2.2.12 on 2020-04-28 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20200428_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Date published'),
        ),
    ]
