from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, NewListingForm



from .models import User, AuctionListing, Bid, Comment, Watchlist


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.all()
         
        
        })
    
def listing(request, listing):
    # call model object and pass on to the template
    cf = CommentForm(request.POST or None) 
    listing = AuctionListing.objects.get(listname=listing)
    bid= Bid.objects.get(bid_item=listing.listname)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid": Bid.objects.get(bid_item=listing.listname),
        "comment":listing.comments.all(),
        "comment_form": cf
        
        })
        
@login_required
def bid(request, listing):
    user = request.user.username
    cf = CommentForm(request.POST or None) 
    if request.method == "POST":
        bid = request.POST["bid"]
        listing = AuctionListing.objects.get(listname=listing)
        originalbid = Bid.objects.get(bid_item=listing.listname)
        
        
        auctionprice = originalbid.bid_amount
        if int(bid) > int(auctionprice):
            bid = request.POST["bid"]
            originalbid = Bid.objects.get(bid_item=listing.listname)
            originalbid.bid_amount =  int(bid)
            originalbid.save()
           
            listing.winner = user
            listing.save()
           
            return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid": Bid.objects.get(bid_item=listing.listname),
            "bidmessage": "You Bid Succesfully!",
            "comment":listing.comments.all(),
            "comment_form": cf 
            
        })

        else: 
            return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid": Bid.objects.get(bid_item=listing.listname),
            "bidmessage": "Bid must be greater than current bid",
            "comment":listing.comments.all(),
            "comment_form": cf
        
        })

       
        
def create_comment(request, listing): 
    if request.method == 'POST': 
        cf = CommentForm(request.POST or None) 
        if cf.is_valid(): 
          new_comment = request.POST.get('new_comment') 
          item = request.POST.get('item')
          listing = AuctionListing.objects.get(listname=listing)
          comment = Comment.objects.create(item = listing, user = request.user, new_comment = new_comment) 
          comment.save() 
          return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid": Bid.objects.get(bid_item=listing.listname),
            "comment":listing.comments.all(),
            "comment_form": cf
            })
    else: 
        cf = CommentForm() 
        context ={'comment_form':cf,} 
    
def new_listing(request):
    cf = NewListingForm(request.POST, request.FILES) 
    return render(request, "auctions/newlisting.html", {
    "newcomment_form": cf
    })

def createnew_listing(request):
    if request.method == 'POST' or request.method =="FILES": 
        listname = request.POST.get('listname') 
        description = request.POST.get('description')
        image= request.FILES.get('image')
        price = request.POST.get('price')
        category=request.POST.get('category')
        newlisting = AuctionListing.objects.create(listname = listname, description = description, image =  image, price = price, category=category) 
        newlisting.save()
        
        newbid = Bid.objects.create(bid_item=newlisting, bid_amount=price, bidder_id=True) 
        newbid.save()
          
        return render(request, "auctions/index.html", {
            "listings": AuctionListing.objects.all()
            })
   
    
def closebid(request, listing):

    listing = AuctionListing.objects.get(listname=listing)
    listing.delete()
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.all()
        
        })
     
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlistings": Watchlist.objects.filter(watch_user=request.user),
        "listings": AuctionListing.objects.all()
        })
        
@login_required
def addwatchlist(request, listing):
    listing = AuctionListing.objects.get(listname=listing)
    cf = CommentForm(request.POST or None)
    try:
        Watchlist.objects.get(watchlist_item=listing, watch_user=request.user)
    except:
        new = Watchlist.objects.create(watchlist_item=listing, watch_user = request.user)
        new.save()
      
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid": Bid.objects.get(bid_item=listing.listname),
        "comment":listing.comments.all(),
        "comment_form": cf,
        "message": "Added Succesfully to Watchlist",
        })
        
def categories(request):
    return render(request, "auctions/categories.html", {
        "listings": AuctionListing.objects.values('category').distinct()
        })
        
        
        
def categorypage(request, listing):
    listing = AuctionListing.objects.filter(category=listing)
    return render(request, "auctions/categorypage.html", {
    "thecategory": listing
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
