from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Bid, Comment, Category
from django.contrib import messages
from decimal import Decimal

def watchlist(request):
    user = request.user
    watchlist_items = user.watchlist.all()

    return render(request, "auctions/watchlist.html", {
        "watchlist_items": watchlist_items
    })

def add_to_watchlist(request,listing_id):
    if request.user.is_authenticated:
        listing = get_object_or_404(Listing, id=listing_id)
        request.user.watchlist.add(listing)
        return redirect('listing_detail', listing_id=listing_id)
    return redirect('login')

def remove_from_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.user.is_authenticated:
        request.user.watchlist.remove(listing)
    return redirect('listing_detail', listing_id=listing_id)


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
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
        title = request.POST.get("title")
        description = request.POST.get("description")
        starting_bid = request.POST.get("starting_bid")
        image_url = request.POST.get("image_url")
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id)

        listing = Listing(
            title=title, 
            description=description,
            starting_bid=starting_bid,
            image_url=image_url,
            category=category,
            created_by=request.user
        )
        listing.save()

        return redirect("index")
    categories = Category.objects.all()
    return render(request, "auctions/create_listing.html", {
        "categories": categories
    })

def listing_detail(request, listing_id):
    # print(f"Received request for {listing_id}")
    listing = get_object_or_404(Listing, id=listing_id)
    is_in_watchlist = False
    message = None
    message_type = None
    user_is_winner = False

    if request.user.is_authenticated:
        is_in_watchlist = listing in request.user.watchlist.all()
    # print(f"Rendering {listing.title}")

        if not listing.is_active and listing.winner == request.user:
            user_is_winner = True 

    if request.method == "POST":
        if "close" in request.POST:
            if request.user == listing.created_by:
                highest_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()
                if highest_bid:
                    listing.is_active = False
                    listing.winner = highest_bid.bidder
                    listing.win_amount = highest_bid.amount
                    listing.save()
                    message = f"Auction is closed. The highest bidder is {highest_bid.bidder.username}"
                    message_type = "success"
                    
                    
                else:
                    message = "No bids have been placed yet"
                    message_type = "error"
                    
        elif "comment" in request.POST:
            comment_text = request.POST.get("comment_text")
            if comment_text:
                Comment.objects.create(
                    listing=listing, 
                    user=request.user,
                    text=comment_text
                )
                message = "Comment added successfully"
                message_type = "success"
            else:
                message = "Comment cannot be empty"
                message_type = "error"


    bids = Bid.objects.filter(listing=listing).order_by('-amount')  
    comments = listing.comments.all().order_by('-timestamp')  

    return render(request, "auctions/listing_detail.html", {
        "listing": listing,
        "is_in_watchlist": is_in_watchlist,
        "message": message,
        "message_type": message_type,
        "bids": bids,
        "user_is_winner": user_is_winner,
        "comments": comments
    })

def bid_on_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    message = None
    message_type = None
    if request.method == "POST":
        amount_str = request.POST.get("amount")
        try:
            amount = Decimal(amount_str)
        except:
            message = "Invalid Bid Amount"
            message_type = "error"
        if not message:
            if amount < listing.starting_bid:
                message = "Bid must be at least as large as the starting bid"
                message_type = "error"
            else:
                highest_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()
                if highest_bid and amount <= highest_bid.amount:
                    message = "Bid must be higher than current bid"
                    message_type = "error"
                else:
                    Bid.objects.create(
                        listing=listing,
                        bidder=request.user,
                        amount=amount
                    )
                    message = "Bid placed successfully"
                    message_type = "success"

    bids = Bid.objects.filter(listing=listing).order_by('-amount')    

    context = {
        "listing": listing, 
        "message": message,
        "message_type": message_type,
        "bids": bids
    }   

    return render(request, "auctions/listing_detail.html", context)


def category(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_listings(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    listings = Listing.objects.filter(category=category, is_active=True)
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings
    })