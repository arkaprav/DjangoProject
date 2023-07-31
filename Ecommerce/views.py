from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.conf import settings
from products.models import Category, Brand, Product
from django.db.models import Min, Max
import json
import os
def home(request):
    c = Category.objects.all().exclude(num_products=0)
    p = Product.objects.all().order_by('-rating')
    b = Brand.objects.all().exclude(num_products=0)
    title = {
        'title': 'Home',
        'c': c,
        'p': p,
        'b': b,
        'media_link':settings.MEDIA_URL
    }
    return render(request,'index.html',context=title)
def contact(request):
    c = Category.objects.all().exclude(num_products=0)
    b = Brand.objects.all().exclude(num_products=0)
    title = {
        'title': 'Contact',
        'c': c,
        'b': b,
    }
    return render(request,'contact.html',context=title)
def shop(request):
    if request.method == 'POST':
        price = request.POST.get('price',0)
        brands = request.POST.getlist('brands[]')
        categories = request.POST.getlist('categories[]')
        results = list(Product.objects.all().values())
        for i in range(len(results)):
            category = list(Category.objects.filter(id__exact = results[i]['category_id']).values_list()[0])
            results[i]['category'] = category[1]
            brand = list(Brand.objects.filter(id__exact = results[i]['brand_id']).values_list()[0])
            results[i]['brand'] = brand[1]
        if price != 0:
            if(categories != [] or brands != []):
                answer = []
                for i in range(len(results)):
                    if results[i]['price'] <= float(price) and (results[i]['category'] in categories or results[i]['brand'] in brands):
                        answer.append(results[i])
                return JsonResponse(list(answer),safe=False, status=200)
            else:
                answer = []
                for i in range(len(results)):
                    if results[i]['price'] <= float(price):
                        answer.append(results[i])
                return JsonResponse(list(answer),safe=False, status=200)         
    c = Category.objects.all().exclude(num_products=0)
    p = Product.objects.all()
    b = Brand.objects.all().exclude(num_products=0)
    min_value = Product.objects.aggregate(Min('price'))['price__min']
    max_value = Product.objects.aggregate(Max('price'))['price__max']
    print(min_value, max_value)
    title = {
        'title': 'Shop',
        'c': c,
        'p': p,
        'b': b,
        'min': int(min_value),
        'max': int(max_value),
        'media_link':settings.MEDIA_URL
    }
    return render(request,'shop.html',context=title)