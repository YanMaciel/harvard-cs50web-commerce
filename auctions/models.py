from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Item(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    
