from asyncio.windows_events import NULL
from contextlib import nullcontext
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.db.models import Max
from django.contrib.auth.decorators import login_required


# There is an error where when u post a comment or a bid and refresh the page, the form of either
# bid or comment keeps adding itself again 
# This can be solved by replacing all html forms with form classes by Django to make validations by its own 
# im just lazy to do this, sorry :c



def listing(request, id):
    currentListing = Listing.objects.get(id = id)
    AllComments = Comment.objects.filter(listings = currentListing)
    AllBids = Bid.objects.filter(listings = currentListing)
    return render(request, "auctions/listing.html",{
        "listing": currentListing,
        "comments": AllComments,
        "bids" :AllBids
    })


def AddComment(request, id):
    if request.method == 'POST':
        commentContent = request.POST["comment"]
        currentListing = Listing.objects.get(id = id)
        username = request.user
        NewComment = Comment(
            commentContent = commentContent,
            listings = currentListing,
            user = username
        )
        AllComments = Comment.objects.filter(listings = currentListing)
        AllBids = Bid.objects.filter(listings = currentListing)
        if len(commentContent) <=1:
            return render(request, "auctions/listing.html",{
                "listing": currentListing,
                "comments": AllComments,
                "bids": AllBids,
                "errorComment": "Please put a comment first!"
            })
        else:
            NewComment.save()
            return render(request, "auctions/listing.html",{
                "listing": currentListing,
                "comments": AllComments,
                "bids": AllBids
            })


def AddBid(request, id):
    if request.method == 'POST':
        BidAmount = request.POST["bid"]
        currentListing = Listing.objects.get(id = id)
        username = request.user
        NewBid = Bid(
            bidAmount = BidAmount,
            listings = currentListing,
            user = username
        )
        AllBids = Bid.objects.filter(listings = currentListing)
        MaxBid = AllBids.aaggregate(Max(''))
        AllComments = Comment.objects.filter(listings = currentListing)
        if len(BidAmount) <=1:
            return render(request, "auctions/listing.html",{
            "listing": currentListing,
            "comments": AllComments,
            "bids": AllBids,
            "errorBid": "Please put a bid first!"
        })
        else:
            NewBid.save()
            return render(request, "auctions/listing.html",{
                "listing": currentListing,
                "comments": AllComments,
                "bids": AllBids
            })




@login_required
def create(request):
    if request.method == 'POST':
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        price = request.POST["price"]
        category = request.POST["category"]
        currentUser = request.user
        categoryData = Category.objects.get(categoryName = category)
        newListing = Listing(
            title = title,
            description = description,
            image = image,
            price = float(price),
            owner = currentUser,
            category = categoryData,
        )
        newListing.save()
        return HttpResponseRedirect(reverse("index"))
    allCategories = Category.objects.all()

    return render(request, "auctions/create.html",{
        "categories": allCategories
    })


def categorySelection(request):
    if request.method == 'POST':
        categoryForm = request.POST["category"]
        categorySelected = Category.objects.get(categoryName = categoryForm)
        return render(request, "auctions/index.html",{
            "Listings": Listing.objects.filter(isActive = True, category = categorySelected),
            "categories": Category.objects.all(),
        })
    else:
     return HttpResponseRedirect(reverse("index"))


def index(request):
    return render(request, "auctions/index.html",{
        "Listings": Listing.objects.filter(isActive = True),
        "categories": Category.objects.all()
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
