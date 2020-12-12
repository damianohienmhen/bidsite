from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField(max_length=64, default="")
    

class AuctionListing(models.Model):
    CATEGORIES = (
           ('FOT', 'Footwear'),
           ('CLO', 'Clothes'),
           ('INT', 'Instruments'),
           ('ELE', 'Electronics'),
           ('OTH', 'Other')
    )
    listname = models.CharField(primary_key = True, max_length=64, default="")
    image = models.ImageField(upload_to ='media/images', default="")
    description = models.CharField(max_length=25, default="")
    price = models.IntegerField()
    category = models.CharField(max_length=10, choices=CATEGORIES, default="" )
    date_posted = models.DateTimeField(auto_now_add=True, null= True, blank=True) 
    winner=models.CharField(max_length=10, default="")
    
    def __str__(self):
        return f"{self.listname} ({self.price})"
        
class Bid(models.Model):
    bidder=models.ForeignKey(User, on_delete=models.CASCADE)
    bid_item= models.ForeignKey(AuctionListing,on_delete=models.CASCADE)
    bid_amount=models.IntegerField(null=True)
    
    def __str__(self):
        return f"{self.bidder} ({self.bid_item})"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users', default="")
    item= models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='comments')
    new_comment= models.TextField()
    
    def __str__(self):
        return f"{self.item} ({self.new_comment})"
        
class Watchlist(models.Model):
    watchlist_item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='watchlist')
    watch_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchusers', default="")
    
    def __str__(self):
        return f"{self.watch_user}: {self.watchlist_item}"
    
    
   
    

    
    
    
    
    