
from products.models import Category, Brand, Product
from django.shortcuts import get_object_or_404
from django.db.models import Min, Max
from django.conf import settings

#get category wise products
def get_category(keys,fav, login, slug, c, b):
        post = get_object_or_404(Category, slug=slug)
        p = Product.objects.filter(category=post)
        pro = list(p.values())
        brands  = []
        for i in range(len(pro)):
            brands.append(pro[i]['brand_id'])
        min_value = Product.objects.filter(category=post).aggregate(Min('price'))['price__min']
        max_value = Product.objects.filter(category=post).aggregate(Max('price'))['price__max']
        y = Brand.objects.filter(id__in = brands).exclude(num_products=0)
        title={
            'title':post,
            'c': c,
            'p': p,
            'b': b,
            'y': y,
            'login': login,
            'min': int(min_value),
            'max': int(max_value),
            'cart_items':keys,
            'fav_items':fav,
            'media_link':settings.MEDIA_URL
        }
        return title

#get brand wise products
def get_brand(keys, fav, login, slug, c, b):
    post = get_object_or_404(Brand, slug=slug)
    p = Product.objects.filter(brand=post)
    pro = list(p.values())
    cats  = []
    for i in range(len(pro)):
        cats.append(pro[i]['category_id'])
    min_value = Product.objects.filter(brand=post).aggregate(Min('price'))['price__min']
    max_value = Product.objects.filter(brand=post).aggregate(Max('price'))['price__max']
    x = Category.objects.filter(id__in = cats).exclude(num_products=0)
    title={
        'title':post,
        'c': c,
        'p': p,
        'b': b,
        'x': x,
        'login': login,
        'min': int(min_value),
        'max': int(max_value),
        'cart_items':keys,
        'fav_items':fav,
        'media_link':settings.MEDIA_URL
    }
    return title