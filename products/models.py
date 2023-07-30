from django.db import models
from autoslug import AutoSlugField

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
