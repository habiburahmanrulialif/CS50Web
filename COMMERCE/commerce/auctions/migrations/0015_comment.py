# Generated by Django 4.2.6 on 2023-12-03 00:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_listing_date_post_bid'),
    ]

    operations = [
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('post_date', models.TimeField(auto_now_add=True)),
                ('comment_listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing')),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
