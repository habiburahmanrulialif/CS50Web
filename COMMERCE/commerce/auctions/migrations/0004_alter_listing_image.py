# Generated by Django 4.2.6 on 2023-11-30 06:41

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=-1, scale=None, size=[500, 300], upload_to='auctions/static/auctions/image'),
        ),
    ]
