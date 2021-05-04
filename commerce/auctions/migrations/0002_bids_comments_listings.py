# Generated by Django 3.1.7 on 2021-04-23 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=64)),
                ('listingid', models.IntegerField()),
                ('bid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('time', models.CharField(max_length=64)),
                ('comment', models.TextField()),
                ('listingid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Listings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=64)),
                ('seller', models.CharField(max_length=64)),
                ('startting_bid', models.IntegerField()),
                ('description', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(max_length=64)),
                ('image_link', models.CharField(blank=True, default=None, max_length=200, null=True)),
            ],
        ),
    ]
