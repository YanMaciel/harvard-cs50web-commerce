
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Item, Bid


def index(request):
    active_listings = Item.objects.all()
    current_prices = Bid.objects.order_by().values_list('product').distinct()
    print(current_prices)
    return render(request, "auctions/index.html", {
        "active_listings": active_listings,
        "current_prices": current_prices
    })


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

@login_required
def create_listing(request):
    if request.method == "POST":
        if request.POST["price"].isdigit():
            listing = Item(
                title=request.POST["title"],
                description=request.POST["description"],
                image_url=request.POST["image_url"],
                category=request.POST["category"],
                owner=User(id=request.user.id)
            )
            listing.save()
            
            start_price = Bid(
                bid_price=float(request.POST["price"]),
                owner=User(id=request.user.id),
                product=Item(id=listing.id)
            )
            start_price.save()
            print(Bid.objects.filter(id=start_price.id))
        else:
            return render(request, "auctions/create_listing.html", {
                "error": "error"
            })
    
    # print(Item.objects.filter(owner=request.user.id))
    return render(request, "auctions/create_listing.html")

def listings(request, listing_id):
    
    listing = Item.objects.get(id=listing_id)
    current_price = Bid.objects.filter(id=listing_id).latest('id')
    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_price": current_price
    })
    
