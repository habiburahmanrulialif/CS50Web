from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import User, comment, bid, category as categorys, listing as listing_2
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .forms import listingForm, bidForm, commentForm
from django.contrib import messages

def index(request):
    auction = listing_2.objects.all()
    return render(request, "auctions/index.html", {'listing' : auction})


def Category(request):
    if request.method == "POST":
        instance = categorys.objects.all()
        q = request.POST['choices'].lower()
        choice = listing_2.objects.filter(category=q)
        return render(request, "auctions/category.html", {'category' : instance, 'listing' : choice})
    else:
        instance = categorys.objects.all()
        return render(request, "auctions/category.html", {'category' : instance})


def listing(request, id):
    listing_1 = listing_2.objects.get(id=id)
    commentList = comment.objects.filter(comment_listing = listing_1)
    if request.user == listing_1.owner:
        owner = True
    else:
        owner = False
    if request.user == listing_1.winner:
        winning = True
    else:
        winning = False
    if request.method == "GET":
        biddingForm = bidForm()
        commentingForm = commentForm()
        if listing_1 is not None:
            if request.user:
                user_instance = User.objects.get(username=request.user)
                wishCheck = user_instance.wishlist.all()
                if listing_1 in wishCheck:
                    wishCheck_1 = True
                else:
                    wishCheck_1 = False
                return render(request, "auctions/listing.html", {'listing': listing_1, 'bidForm' : biddingForm, 'commentForm' : commentingForm, 'comments' : commentList, 'owner' : owner, 'winning':winning, 'wish' : wishCheck_1})
            else:
                return render(request, "auctions/listing.html", {'listing': listing_1, 'bidForm' : biddingForm, 'commentForm' : commentingForm, 'comments' : commentList, 'owner' : owner, 'winning':winning})
        else:
            raise Http404('List does not exist')
    else:
        biddingForm = bidForm(request.POST)
        commentingForm = commentForm(request.POST)
        if biddingForm.is_valid():
            instance = biddingForm.save(commit=False)
            if request.user == listing_1.owner:
                messages.error(request, 'You cant bid on your own auction')
                return render(request, "auctions/listing.html", {'listing': listing_1, 'bidForm' : biddingForm, 'commentForm' : commentingForm, 'comments' : commentList, 'owner' : owner, 'winning':winning})
            else:
                if instance.bid_amount <= listing_1.starting_price:
                    messages.error(request, 'please bid more than the price of the item')
                    return render(request, "auctions/listing.html", {'listing': listing_1, 'bidForm' : biddingForm, 'commentForm' : commentingForm, 'comments' : commentList, 'owner' : owner, 'winning':winning})
                else:
                    instance.bidder = request.user
                    instance.bid_listing = listing_1
                    instance.save()
                    listing_1.starting_price = instance.bid_amount
                    listing_1.winner = request.user
                    listing_1.save()
                    messages.success(request, 'Bid succesfully add')
                    return render(request, "auctions/listing.html", {'listing': listing_1, 'bidForm' : biddingForm, 'commentForm' : commentingForm, 'comments' : commentList, 'owner' : owner, 'winning':winning})
        elif commentingForm.is_valid():
            instance = commentingForm.save(commit=False)
            instance.commenter = request.user
            instance.comment_listing = listing_1
            instance.save()
            messages.success(request, 'comment added!')
            return render(request, "auctions/listing.html", {'listing': listing_1, 'bidForm' : biddingForm, 'commentForm' : commentingForm, 'comments' : commentList, 'owner' : owner, 'winning':winning})
        
        
        else:
            messages.error(request, 'something wrong')
            return render(request, "auctions/listing.html", {'listing': listing_1, 'bidForm' : biddingForm, 'commentForm' : commentingForm, 'comments' : commentList, 'owner' : owner, 'winning':winning})


def unlist(request, id):
    wish_1 = get_object_or_404(listing_2, id=id)
    wish_1.status = False
    wish_1.save()
    messages.success(request, 'Item listing succesfully closed.')
    return HttpResponseRedirect(reverse('listing',kwargs={
            'id': id,
        }))


@login_required
def wish(request, id):
    wish_1 = get_object_or_404(listing_2, id=id)
    wish_2 = request.user.wishlist.all()
    if wish_1 in wish_2:
        request.user.wishlist.remove(wish_1)
        request.user.save()
        messages.success(request, 'Item succesfully remove to watchlist!')
        return HttpResponseRedirect(reverse('listing',kwargs={
                'id': id
            }))
    else:
        request.user.wishlist.add(wish_1)
        request.user.save()
        messages.success(request, 'Item succesfully added from watchlist!')
        return HttpResponseRedirect(reverse('listing',kwargs={
                'id': id
            }))


@login_required
def wishlist(request):
    auction = request.user.wishlist.all()
    return render(request, "auctions/index.html", {'listing' : auction})


@login_required
def yourAuction(request):
    auction = listing_2.objects.filter(owner=request.user)
    return render(request, "auctions/yourAuction.html", {'listing' : auction})


@login_required
def create(request):
    if request.method == "GET":
        form = listingForm()
        return render(request, "auctions/create.html", {'form': form})
    else:
        form = listingForm(request.POST, request.FILES)
        print("Form data:", request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            return HttpResponseRedirect(reverse("index"))   
        else:
            print(form.errors)
            return render(request, "auctions/create.html", {'form': form, 'errors': form.errors})


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
