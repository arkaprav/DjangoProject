from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.conf import settings
from products.models import Category, Brand, Product
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
        data = request.POST.get('data',0)
        if data != 0:
            results = Product.objects.filter(price__range = ( 0, float(data)) ).values()
            return JsonResponse(list(results),safe=False, status=200)
    c = Category.objects.all().exclude(num_products=0)
    p = Product.objects.all()
    b = Brand.objects.all().exclude(num_products=0)
    title = {
        'title': 'Shop',
        'c': c,
        'p': p,
        'b': b,
        'media_link':settings.MEDIA_URL
    }
    return render(request,'shop.html',context=title)