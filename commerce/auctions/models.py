from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime   

class User(AbstractUser):
    pass
class Listings(models.Model):
    Name = models.CharField(max_length=64)
    seller = models.CharField(max_length=64)
    current_bid= models.IntegerField()
    description=models.TextField()
    time=models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=64)
    image_link = models.CharField(max_length=200, default=None, blank=True, null=True)
    #max_bid=models.IntegerField(blank=True,null=True)
    def __str__(self):
        return 'Listings: {}'.format(self.Name)
class Bids(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    listingid = models.IntegerField()
    bid = models.IntegerField()
class Comments(models.Model):
    user = models.CharField(max_length=64)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    listingid = models.IntegerField()
class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    productid = models.IntegerField(null=False)
class Winner(models.Model):
    owner=models.CharField(max_length=64)
    winner=models.CharField(max_length=64)
    productid = models.IntegerField()
    winning_cost = models.IntegerField()
    name = models.CharField(max_length=64, null=True)



