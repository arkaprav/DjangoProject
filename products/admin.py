from django.contrib import admin
from products.models import Category, Brand, Product, UserProfile, Items, Order
# # Register your models here.

class Category_Admin(admin.ModelAdmin):
    list_display = ('name','description','num_products','featured_image','slug')

class Brand_Admin(admin.ModelAdmin):
    list_display = ('name','description','num_products','featured_image','slug')

class Product_Admin(admin.ModelAdmin):
    list_display = ('name','description','featured_image','category','brand','price','rating','slug')

class UserProfile_Admin(admin.ModelAdmin):
    list_display = ('user_id','user_name','get_cart','get_orders','get_favourites')

class Items_Admin(admin.ModelAdmin):
    list_display = ('item_id', 'item_quantity')
    
class Order_Admin(admin.ModelAdmin):
    list_display = ('user_id', 'get_order_items','PaymentStatus','Address')
    
admin.site.register(Category, Category_Admin)
admin.site.register(Brand, Brand_Admin)
admin.site.register(Product, Product_Admin)
admin.site.register(UserProfile, UserProfile_Admin)
admin.site.register(Items, Items_Admin)
admin.site.register(Order, Order_Admin)