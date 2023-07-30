from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product, Category

@receiver(post_save, sender=Product)
def update_num_products(sender, instance, created, **kwargs):
    instance.category.num_products = Product.objects.filter(category=instance.category).count()
    instance.category.save()
    instance.brand.num_products = Product.objects.filter(brand=instance.brand).count()
    instance.brand.save()

@receiver(post_delete, sender=Product)
def update_num_products(sender, instance, **kwargs):
    instance.category.num_products = Product.objects.filter(category=instance.category).count()
    instance.category.save()
    instance.brand.num_products = Product.objects.filter(brand=instance.brand).count()
    instance.brand.save()