# Generated by Django 4.1.1 on 2022-09-20 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_profile_address_profile_first_name_profile_last_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
    ]