from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.conf import settings
from django.contrib.auth.models import User
from products.models import Category, Brand, Product
from django.db.models import Min, Max
from django.contrib.auth.forms import UserCreationForm
import json
import os
from datetime import datetime, timedelta
def home(request):
    p_center = 0
    c_center = 0
    b_center = 0
    c = Category.objects.all().exclude(num_products=0)
    p = Product.objects.all().order_by('-rating')
    b = Brand.objects.all().exclude(num_products=0)
    if len(list(p.values())) > 3:
        p_center = 1
    if len(list(c.values())) > 3:
        c_center = 1
    if len(list(b.values())) > 3:
        b_center = 1
    title = {
        'title': 'Home',
        'c': c,
        'p': p,
        'b': b,
        'p_center':p_center,
        'c_center':c_center,
        'b_center':b_center,
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
def taxonomy(request, taxonomy_slug):
    try:
        post = get_object_or_404(Category, slug=taxonomy_slug)
        c = Category.objects.all().exclude(num_products=0)
        p = Product.objects.filter(category=post)
        pro = list(p.values())
        brands  = []
        for i in range(len(pro)):
            brands.append(pro[i]['brand_id'])
        min_value = Product.objects.aggregate(Min('price'))['price__min']
        max_value = Product.objects.aggregate(Max('price'))['price__max']
        b = Brand.objects.all().exclude(num_products=0)
        y = Brand.objects.filter(id__in = brands).exclude(num_products=0)
        title={
            'title':post,
            'c': c,
            'p': p,
            'b': b,
            'y': y,
            'min': int(min_value),
            'max': int(max_value),
            'media_link':settings.MEDIA_URL
        }
    except:
        post = get_object_or_404(Brand, slug=taxonomy_slug)
        c = Category.objects.all().exclude(num_products=0)
        p = Product.objects.filter(brand=post)
        pro = list(p.values())
        cats  = []
        for i in range(len(pro)):
            cats.append(pro[i]['category_id'])
        min_value = Product.objects.aggregate(Min('price'))['price__min']
        max_value = Product.objects.aggregate(Max('price'))['price__max']
        b = Brand.objects.all().exclude(num_products=0)
        x = Category.objects.filter(id__in = cats).exclude(num_products=0)
        title={
            'title':post,
            'c': c,
            'p': p,
            'b': b,
            'x': x,
            'min': int(min_value),
            'max': int(max_value),
            'media_link':settings.MEDIA_URL
        }
    return render(request, 'taxonomy.html', context=title)
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                previous_url = request.session.pop('previous_url', None)
                if previous_url:
                    response = redirect(previous_url)# Redirect to the user's profile page after successful registration
                    expiration_time = datetime.now() + timedelta(days=30)  
                    response.set_cookie('user_id', user.id, expires=expiration_time)
                    return response
                else:
                    response = redirect('profile')
                    expiration_time = datetime.now() + timedelta(days=30)  
                    response.set_cookie('user_id', user.id, expires=expiration_time)
                    return response
    else:
        form = UserCreationForm()
    c = Category.objects.all().exclude(num_products=0)
    b = Brand.objects.all().exclude(num_products=0)
    title = {
        'title': 'Register',
        'c': c,
        'b': b,
        'form': form
    }
    return render(request, 'register.html', title)
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            previous_url = request.session.pop('previous_url', None)
            if previous_url:
                response = redirect(previous_url)# Redirect to the user's profile page after successful registration
                expiration_time = datetime.now() + timedelta(days=30)  
                response.set_cookie('user_id', user.id, expires=expiration_time)
                return response
            else:
                response = redirect('profile')
                expiration_time = datetime.now() + timedelta(days=30)  
                response.set_cookie('user_id', user.id, expires=expiration_time)
                return response
    c = Category.objects.all().exclude(num_products=0)
    b = Brand.objects.all().exclude(num_products=0)
    title = {
        'title': 'login',
        'c': c,
        'b': b,
    }
    return render(request, 'login.html', title)
def profile(request):
    if request.user.is_authenticated:
        username = request.user.username
        c = Category.objects.all().exclude(num_products=0)
        b = Brand.objects.all().exclude(num_products=0)
        title = {
            'title': 'profile',
            'c': c,
            'b': b,
            'username':username
        }
        return render(request, 'profile.html', title)
    else:
        if request.COOKIES:
            user_id = request.COOKIES.get('user_id')
            if user_id:
                user = User.objects.get(pk=user_id)
                if user:
                    login(request, user)
        else:
            request.session['previous_url'] = request.get_full_path()
        return redirect('login')