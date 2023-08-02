from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    num_products = models.PositiveIntegerField(default=0)
    featured_image  =  models.FileField(upload_to="category/", max_length = 50, null=True, default=None)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name
    

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    num_products = models.PositiveIntegerField(default=0)
    featured_image  =  models.FileField(upload_to="brand/", max_length = 50, null=True, default=None)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name            = models.CharField(max_length=100)
    description     = models.TextField()
    featured_image  = models.FileField(upload_to="product/", max_length = 50, null=True, default=None)
    category        = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    brand           = models.ForeignKey(Brand, null=True, blank=True, on_delete=models.SET_NULL)
    price           = models.FloatField()
    rating          = models.FloatField()
    slug = AutoSlugField(populate_from='name')
    # Other product fields

    def __str__(self):
        return self.name

class Items(models.Model):
    item_id = models.TextField()

class Order(models.Model):
    order_id = models.IntegerField()

class Favourite(models.Model):
    favourite_id = models.IntegerField()

class UserProfile(models.Model):
    user_id     = models.IntegerField()
    user_name   = models.CharField(max_length=50)
    cart        = models.ManyToManyField(Items, blank = True)
    orders      = models.ManyToManyField(Order, blank = True)
    favourites  = models.ManyToManyField(Favourite, blank = True)
    
    def get_cart(self):
        return ','.join([p.item_id  for p in self.cart.all()])
    
    def get_orders(self):
        return ','.join([p.order_id  for p in self.orders.all()])
    
    def get_favourites(self):
        return ','.join([p.favourite_id  for p in self.favourites.all()])