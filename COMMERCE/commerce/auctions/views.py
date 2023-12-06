from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, comment, bid, category as categorys, listing as listing_2
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .forms import listingForm, bidForm, commentForm
from django.contrib import messages

def index(request):
    auction = listing_2.objects.all()
    return render(request, "auctions/index.html", {'listing' : auction})




@login_required
def yourAuction(request):
    auction = listing_2.objects.filter(owner=request.user)
    return render(request, "auctions/yourAuction.html", {'listing' : auction})


def Category(request):
    if request.method == "POST":
        instance = categorys.objects.all()
        q = request.POST['choices'].lower()
        choice = listing_2.objects.filter(category=q)
        return render(request, "auctions/category.html", {'category' : instance, 'listing' : choice})
    else:
        instance = categorys.objects.all()
        return render(request, "auctions/category.html", {'category' : instance})


@login_required
def create(request):
    if request.method == "GET":
        form = listingForm()
        return render(request, "auctions/create.html", {'form': form})
    else:
        form = listingForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
        return HttpResponseRedirect(reverse("index"))   


def listing(request, id):
    listing_1 = listing_2.objects.get(id=id)
    commentList = comment.objects.filter(comment_listing = listing_1)
    if request.method == "GET":
        biddingForm = bidForm()
        commentingForm = commentForm()
        if listing_1 is not None:
            return render(request, "auctions/listing.html", {'listing': listing_1, 'bidForm' : biddingForm, 'commentForm' : commentingForm, 'comments' : commentList})
        else:
            raise Http404('List does not exist')
    else:
        biddingForm = bidForm(request.POST)
        commentingForm = commentForm(request.POST)
        if biddingForm.is_valid():
            instance = biddingForm.save(commit=False)
            if request.user == listing_1.owner:
                messages.error(request, 'You cant bid on your own auction')
                return render(request, "auctions/listing.html", {'listing': listing_1, 'bidForm' : biddingForm, 'commentForm' : commentingForm, 'comments' : commentList})
            else:
                if instance.bid_amount <= listing_1.starting_price:
                    messages.error(request, 'please bid more than the price of the item')
                    return render(request, "auctions/listing.html", {'listing': listing_1, 'bidForm' : biddingForm, 'commentForm' : commentingForm, 'comments' : commentList})
                else:
                    instance.bidder = request.user
                    instance.bid_listing = listing_1
                    instance.save()
                    listing_1.starting_price = instance.bid_amount
                    listing_1.winner = request.user
                    listing_1.save()
                    messages.success(request, 'Bid succesfully add')
                    return render(request, "auctions/listing.html", {'listing': listing_1, 'bidForm' : biddingForm, 'commentForm' : commentingForm, 'comments' : commentList})
        elif commentingForm.is_valid():
            instance = commentingForm.save(commit=False)
            instance.commenter = request.user
            instance.comment_listing = listing_1
            instance.save()
            messages.success(request, 'comment added!')
            return render(request, "auctions/listing.html", {'listing': listing_1, 'bidForm' : biddingForm, 'commentForm' : commentingForm, 'comments' : commentList})
        
        
        else:
            messages.error(request, 'something wrong')
            return render(request, "auctions/listing.html", {'listing': listing_1, 'bidForm' : biddingForm, 'commentForm' : commentingForm, 'comments' : commentList})


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