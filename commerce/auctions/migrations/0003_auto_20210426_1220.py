# Generated by Django 3.1.7 on 2021-04-26 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bids_comments_listings'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listings',
            old_name='startting_bid',
            new_name='starting_bid',
        ),
    ]
