from django.http import HttpResponse
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
    title = {
        'title': 'Contact',
    }
    return render(request,'contact.html',context=title)