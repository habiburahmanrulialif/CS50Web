# Generated by Django 4.2.6 on 2023-12-07 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_alter_listing_owner_alter_listing_winner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='watchlist',
            new_name='wishlist',
        ),
    ]
