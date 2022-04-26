from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Item(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=100)
    image_url = models.CharField(max_length=600)
    category = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_listings")
    
    def __str__(self):
        return f"Item of ID {self.id}, name: {self.title} and owner: {self.owner.username}."
    
    
