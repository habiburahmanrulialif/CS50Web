# Generated by Django 4.2.6 on 2023-12-01 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_listing_owener'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='owener',
            new_name='owner',
        ),
    ]
