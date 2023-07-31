from django.contrib import admin
from products.models import Category, Brand, Product
# Register your models here.

class Category_Admin(admin.ModelAdmin):
    list_display = ('name','description','num_products','featured_image','slug')

class Brand_Admin(admin.ModelAdmin):
    list_display = ('name','description','num_products','featured_image','slug')

class Product_Admin(admin.ModelAdmin):
    list_display = ('name','description','featured_image','category','brand','price','rating','slug')

admin.site.register(Category, Category_Admin)
admin.site.register(Brand, Brand_Admin)
admin.site.register(Product, Product_Admin)