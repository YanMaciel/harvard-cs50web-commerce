from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Item(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=254)
    image_url = models.CharField(max_length=600)
    category = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_listings")
    
    def __str__(self):
        return f"Item of ID {self.id}, name: {self.title} and owner: {self.owner.username}."
    
class Comment(models.Model):
    comment = models.CharField(max_length=254)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_comments")
    product = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="product_comments")
    
    def __str__(self):
        return f"Comment of ID {self.id}, product: {self.product} and owner: {self.owner.username}."
    
class Bid(models.Model):
    bid_price = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_bids")
    product = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="product_bids")
    
    def __str__(self):
        return f"Bid of ID {self.id} and price ${self.bid_price}, product: {self.product} and owner: {self.owner.username}."
    
    
    
    
