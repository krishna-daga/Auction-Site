from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import  Listings,Bids,Comments,Watchlist,Winner
from .models import User
from django.contrib.auth.decorators import login_required
from annoying.functions import get_object_or_None
def index(request):
    # list of products available
    products = Listings.objects.all()
    # checking if there are any products
    empty = False
    if len(products) == 0:
        empty = True
    return render(request, "auctions/index.html", {
        "products": products,
        "empty": empty})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='/login')
def create_listings(request):
    #create listing form
    if request.method=="POST":
        #new object 
        product=Listings()
        #getting each field from the form
        product.seller=request.user.username
        product.Name=request.POST.get('Name')
        product.current_bid=request.POST.get('starting_bid')
        product.description=request.POST.get('description')
        product.category=request.POST.get('category')
        if request.POST.get('image_link'):
            product.image_link=request.POST.get('image_link')
        else:
            product.image_link="https://www.sandu.in/image/cache/catalog/product/no-product-800x800.png"
        #save data in database
        product.save()
        #all the objects in listings
        products=Listings.objects.all()
        empty=False
        if len(products)==0:
            empty = True

        return render(request,"auctions/index.html",{"products": products,
        "empty": empty})
    else:
        return render(request, "auctions/createlisting.html")
#individual listing page
@login_required(login_url='/login')
def listing(request,id):
    #get item based on id
    item=Listings.objects.get(id=id)
    comments=Comments.objects.filter(listingid=id)
    #if bid placed
    if request.method=="POST":
        new_bid=int(request.POST.get('newbid'))
        #check starting one is greater than or equal to bid, object item will have attributes
        if item.current_bid>=new_bid:
            return render(request,"auctions/listing.html",{"msg":"Your bid must be higher than current bid" ,"item":item,"comments":comments,"msg_type":"danger"})
        else:
            item.current_bid=new_bid
            item.save()
            bobj=Bids.objects.filter(listingid=id)
            #if a bid already exists then delete
            if bobj:
                bobj.delete()
            #save 
            bobj=Bids()
            bobj.user=request.user
            bobj.title=item.Name
            bobj.bid=new_bid
            bobj.listingid=id
            bobj.save()
            item_to_save=Listings.objects.get(id=id)
            added = Watchlist.objects.filter(item_to_save, user=request.user)
            return render(request,"auctions/listing.html",{"msg":"Your bid has been successfully placed" ,"item":item,"added":added,"comments":comments})
    else:
        added=Watchlist.objects.filter(user=request.user,item=id)
        return render(request,"auctions/listing.html",{"item":item,"comments":comments, "added":added})
# add watchlist
@login_required(login_url='/login')
def watchlist(request,id):
    item_to_save=Listings.objects.get(id=id)
    obj=Watchlist.objects.filter(user=request.user,item=item_to_save)
    comments=Comments.objects.filter(listingid=id)

    #query to check if the item already exists in watchlist
    if obj.exists():
        obj.delete()
        added=Watchlist.objects.filter(user=request.user,item=item_to_save)
        return render(request,"auctions/listing.html",{"item":item_to_save,"added":added,"comments":comments})
    else:
        watchlist_obj=Watchlist(user=request.user)
        watchlist_obj.save()
        watchlist_obj.item.add(item_to_save)
        added=Watchlist.objects.filter(user=request.user,item=item_to_save)
        return render(request, "auctions/listing.html",{"item":item_to_save,"added":added,"comments":comments})
#view for my watchlist
@login_required(login_url='/login')
def mywatchlist(request):
    #gathering a list for the particular user
    mylist=Watchlist.objects.filter(user=request.user)
    there=False
    list_products=[]
    #if there is a list
    if mylist:
        there=True
        for i in mylist:
            obj=Listings.objects.get(Name=i)
            list_products.append(obj)
        return render(request,"auctions/mywatchlist.html", {"list_products": list_products,"present": there})
    

    else:
        there=False
        return render(request,"auctions/mywatchlist.html", {"list_products": list_products,"present": there})


    
#when seller clicks on closebid button
@login_required(login_url='/login')
def closebid(request,id):
    winobj = Winner()
    listobj = Listings.objects.get(id=id)
    obj = get_object_or_None(Bids, id=id)
    if not obj:
        message = "Deleting Bid"
        msg_type = "danger"
    else:
        bobj = Bids.objects.get(listingid=id)
        winobj.owner = request.user.username
        winobj.winner = bobj.user
        winobj.productid = id
        winobj.winning_cost = bobj.bid
        winobj.name = bobj.title
        winobj.save()
        message = "Bid Closed"
        msg_type = "success"
        # deleting from Bids
        bobj.delete()
    # removing from watchlist
    item=Listings.objects.get(id=id)
    if Watchlist.objects.filter(item=item):
        watchobj = Watchlist.objects.filter(item=id)
        watchobj.delete()
    # removing from Comment
    if Comments.objects.filter(listingid=id):
        commentobj = Comments.objects.filter(listingid=id)
        commentobj.delete()
    # removing from Listing
    listobj.delete()
    # retrieving the new products list after adding and displaying
    # list of products available in WinnerModel
    winners = Winner.objects.all()
    # checking if there are any products
    empty = False
    if len(winners) == 0:
        empty = True
    
    return render(request, "auctions/closedlisting.html", {
        "products": winners,
        "empty": empty,
        
        "message": message,
        "msg_type": msg_type
    })
#to see closed listings
@login_required(login_url='/login')
def closedlisting(request):
    # list of products available in WinnerModel
    winners = Winner.objects.all()
    # checking if there are any products
    empty = False
    if len(winners) == 0:
        empty = True
    return render(request, "auctions/closedlisting.html", {
        "products": winners,
        "empty": empty
    })

def categories(request):
    return render(request,"auctions/categories.html")
def category(request,category):
    #retrieving objects in listing of the category:category 
    category_objs=Listings.objects.filter(category=category)
    if category_objs:

        return render(request,"auctions/category.html",{"category":category,"products":category_objs})
    else:
        return render(request,"auctions/category.html",{"category":category,"products":category_objs,"msg":"No active listings in this category"})
#view to process form and add comment to database
@login_required(login_url='/login')
def addcomment(request,id):
    #create comment object
    new_comment=Comments()
    new_comment.comment=request.POST.get('comment')
    new_comment.listingid=id
    new_comment.user=request.user.username
    new_comment.save()
    item=Listings.objects.get(id=id)
    comments=Comments.objects.filter(listingid=id)
    added=Watchlist.objects.filter(user=request.user,item=id)
    return render(request,"auctions/listing.html",{"item":item,"added":added,"comments":comments})


        