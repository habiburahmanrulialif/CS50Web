# Generated by Django 4.2.6 on 2023-12-01 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_listing_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
