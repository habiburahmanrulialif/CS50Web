# Generated by Django 4.2.6 on 2023-12-06 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_user_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='desc',
            field=models.TextField(blank=True, null=True),
        ),
    ]