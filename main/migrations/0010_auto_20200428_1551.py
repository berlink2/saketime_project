# Generated by Django 2.2.12 on 2020-04-28 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20200428_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile_images/masu_profile.jpg', null=True, upload_to='profile_images'),
        ),
    ]