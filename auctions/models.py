from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=254)
    image_url = models.CharField(max_length=600)
    category = models.CharField(max_length=64)
    created_date = models.DateTimeField(default=timezone.now)
    starting_price = models.FloatField()
    current_bid = models.FloatField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator_listings")
    watchers = models.ManyToManyField(User, blank=True, related_name="watched_listings")
    buyer = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.title} - {self.starting_price}"
    
class Comment(models.Model):
    comment = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="product_comments")
    
    def __str__(self):
        return self.createdDate.strftime('%B %d %Y')
    
class Bid(models.Model):
    offer = models.FloatField()
    created_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.offer} for listing {self.product}"
    
    
    
    
