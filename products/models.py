from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
import json

# Create your models here.

#product categories
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField()
    num_products = models.PositiveIntegerField(default=0)
    featured_image  =  models.FileField(upload_to="category/", max_length = 50, null=True, default=None)
    slug = AutoSlugField(populate_from='name', db_index=True)

    def __str__(self):
        return self.name
    
#product brands
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField()
    num_products = models.PositiveIntegerField(default=0)
    featured_image  =  models.FileField(upload_to="brand/", max_length = 50, null=True, default=None)
    slug = AutoSlugField(populate_from='name', db_index=True)

    def __str__(self):
        return self.name
    
#products
class Product(models.Model):
    name            = models.CharField(max_length=100, db_index=True)
    description     = models.TextField()
    featured_image  = models.FileField(upload_to="product/", max_length = 50, null=True, default=None)
    category        = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, db_index=True)
    brand           = models.ForeignKey(Brand, null=True, blank=True, on_delete=models.SET_NULL, db_index=True)
    price           = models.FloatField(db_index=True)
    rating          = models.FloatField()
    slug = AutoSlugField(populate_from='name', db_index=True)

    def __str__(self):
        return self.name
#single cart,order or favourite items
class Items(models.Model):
    item_id = models.IntegerField(db_index=True)
    item_quantity = models.IntegerField(default=1)

#holds all orders
class Order(models.Model):
    user_id = models.IntegerField()
    order_items =  models.ManyToManyField(Items, blank = True)
    PaymentStatus = models.CharField(max_length=10)
    Status = models.CharField(max_length=20,choices=(
        ("In Progress", "In Progress"),
        ("Cancelled", "Cancelled"),
        ("Completed", "Completed")
    ), default="In Progress")
    Address = models.TextField()
    Date = models.DateTimeField(auto_now_add=True)
    
    def get_order_items(self):
        return ','.join([json.dumps({p.item_id: p.item_quantity})  for p in self.order_items.all()])

#sinfle favourite product
class Favourite(models.Model):
    favourite_id = models.IntegerField(db_index=True)

#user's profileto get cart, order and favourites data
class UserProfile(models.Model):
    user_id     = models.IntegerField(db_index=True)
    user_name   = models.CharField(max_length=50)
    cart        = models.ManyToManyField(Items, blank = True)
    orders      = models.ManyToManyField(Order, blank = True)
    favourites  = models.ManyToManyField(Favourite, blank = True)
    
    def get_cart(self):
        return ','.join([json.dumps({p.item_id: p.item_quantity})  for p in self.cart.all()])
    
    def get_orders(self):
        return ','.join([str(p.id)  for p in self.orders.all()])
    
    def get_favourites(self):
        return ','.join([str(p.favourite_id)  for p in self.favourites.all()])