from django.contrib import admin
from .models import Listings,Bids,Comments,Watchlist,Winner
# Register your models here.
#use admin app to manipualte models
admin.site.register(Listings)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Watchlist)
admin.site.register(Winner)

