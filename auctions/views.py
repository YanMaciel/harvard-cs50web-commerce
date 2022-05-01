
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid


def index(request):
    active_listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "active_listings": active_listings
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
            listing = Listing(
                title=request.POST["title"],
                description=request.POST["description"],
                image_url=request.POST["image_url"],
                category=request.POST["category"],
                starting_price=float(request.POST["price"]),
                creator=User(id=request.user.id)
            )
            listing.save()
            
            return redirect("listings", listing_id=listing.id)
            
        else:
            return render(request, "auctions/create_listing.html", {
                "error": "error"
            })
    
    return render(request, "auctions/create_listing.html")

def listings(request, listing_id):
    
    if not request.user.is_authenticated:
        return redirect("login")
    
    listing = Listing.objects.get(id=listing_id)
    
    if request.method == "POST":
        if request.POST["bid_offer"].isdigit() and float(request.POST["bid_offer"]) > listing.starting_price and (listing.current_bid is None or float(request.POST["bid_offer"]) > listing.current_bid):
            listing.current_bid = float(request.POST["bid_offer"])
            listing.buyer = User(id=request.user.id)
            listing.save()
            
            new_bid = Bid(
                offer = float(request.POST["bid_offer"]),
                owner = User(id=request.user.id),
                product = listing
            )
            new_bid.save()

    return render(request, "auctions/listing.html", {
        "listing": listing,
    })
    
