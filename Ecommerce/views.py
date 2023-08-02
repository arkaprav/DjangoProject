from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.conf import settings
from django.contrib.auth.models import User
from products.models import Category, Brand, Product, UserProfile, Items
from django.db.models import Min, Max
from django.contrib.auth.forms import UserCreationForm
import json
import os
from datetime import datetime, timedelta
def home(request):
    p_center = 0
    c_center = 0
    b_center = 0
    login = 0
    c = Category.objects.all().exclude(num_products=0)
    p = Product.objects.all().order_by('-rating')
    b = Brand.objects.all().exclude(num_products=0)
    if len(list(p.values())) > 3:
        p_center = 1
    if len(list(c.values())) > 3:
        c_center = 1
    if len(list(b.values())) > 3:
        b_center = 1
    if request.user.is_authenticated:
        login = 1
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id, user_name=request.user.username)
        except:
            user_profile = UserProfile.objects.create(user_id=request.user.id, user_name=request.user.username)
        cart_items = user_profile.get_cart()
        item_list = cart_items.split(',')
        keys = []
        for i in item_list:
            item = json.loads(i)
            l=[int(key) for key, value in item.items()]
            keys.append(l[0])
        title = {
            'title': 'Home',
            'c': c,
            'p': p,
            'b': b,
            'p_center':p_center,
            'c_center':c_center,
            'b_center':b_center,
            'login': login,
            'cart_items':keys,
            'media_link':settings.MEDIA_URL
        }
        return render(request,'index.html',context=title)
    elif request.COOKIES:
        user_id = request.COOKIES.get('user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            if user:
                login(request, user)
                login = 1
    else:
        request.session['previous_url'] = request.get_full_path()
        login = 0
    title = {
        'title': 'Home',
        'c': c,
        'p': p,
        'b': b,
        'p_center':p_center,
        'c_center':c_center,
        'b_center':b_center,
        'login': login,
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
            answer = []
            for i in range(len(results)):
                if categories != []:
                    if results[i]['category'] in categories:
                        if brands != []:
                            if results[i]['brand'] in brands:
                                if results[i]['price'] <= float(price):
                                    answer.append(results[i])
                        else:
                            if results[i]['price'] <= float(price):
                                    answer.append(results[i])
                elif brands != []:
                    if results[i]['brand'] in brands:
                        if results[i]['price'] <= float(price):
                                answer.append(results[i])
                else:
                    if results[i]['price'] <= float(price):
                        answer.append(results[i])
            return JsonResponse(list(answer),safe=False, status=200) 
    login = 0
    if request.user.is_authenticated:
        login = 1
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id, user_name=request.user.username)
        except:
            user_profile = UserProfile.objects.create(user_id=request.user.id, user_name=request.user.username)
        c = Category.objects.all().exclude(num_products=0)
        p = Product.objects.all()
        b = Brand.objects.all().exclude(num_products=0)
        min_value = Product.objects.aggregate(Min('price'))['price__min']
        max_value = Product.objects.aggregate(Max('price'))['price__max']
        cart_items = user_profile.get_cart()
        item_list = cart_items.split(',')
        keys = []
        for i in item_list:
            item = json.loads(i)
            l=[int(key) for key, value in item.items()]
            keys.append(l[0])
            
        title = {
            'title': 'Shop',
            'c': c,
            'p': p,
            'b': b,
            'min': int(min_value),
            'max': int(max_value),
            'login': login,
            'cart_items':keys,
            'media_link':settings.MEDIA_URL
        }
        return render(request,'shop.html',context=title)
    elif request.COOKIES:
        user_id = request.COOKIES.get('user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            if user:
                login(request, user)
    else:
        request.session['previous_url'] = request.get_full_path()
        login = 0
        c = Category.objects.all().exclude(num_products=0)
        p = Product.objects.all()
        b = Brand.objects.all().exclude(num_products=0)
        min_value = Product.objects.aggregate(Min('price'))['price__min']
        max_value = Product.objects.aggregate(Max('price'))['price__max']
        title = {
            'title': 'Shop',
            'c': c,
            'p': p,
            'b': b,
            'min': int(min_value),
            'max': int(max_value),
            'login': login,
            'media_link':settings.MEDIA_URL
        }
        return render(request,'shop.html',context=title)        
def taxonomy(request, taxonomy_slug):
    login = 0
    if request.user.is_authenticated:
        login = 1
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id, user_name=request.user.username)
        except:
            user_profile = UserProfile.objects.create(user_id=request.user.id, user_name=request.user.username)
        cart_items = user_profile.get_cart()
        item_list = cart_items.split(',')
        keys = []
        for i in item_list:
            item = json.loads(i)
            l=[int(key) for key, value in item.items()]
            keys.append(l[0])
        try:
            post = get_object_or_404(Category, slug=taxonomy_slug)
            c = Category.objects.all().exclude(num_products=0)
            p = Product.objects.filter(category=post)
            pro = list(p.values())
            brands  = []
            for i in range(len(pro)):
                brands.append(pro[i]['brand_id'])
            min_value = Product.objects.filter(category=post).aggregate(Min('price'))['price__min']
            max_value = Product.objects.filter(category=post).aggregate(Max('price'))['price__max']
            b = Brand.objects.all().exclude(num_products=0)
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
            min_value = Product.objects.filter(brand=post).aggregate(Min('price'))['price__min']
            max_value = Product.objects.filter(brand=post).aggregate(Max('price'))['price__max']
            b = Brand.objects.all().exclude(num_products=0)
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
                'media_link':settings.MEDIA_URL
            }
        return render(request, 'taxonomy.html', context=title)
    elif request.COOKIES:
        user_id = request.COOKIES.get('user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            if user:
                login(request, user)
                login = 1
    else:
        request.session['previous_url'] = request.get_full_path()
        login = 0
        try:
            post = get_object_or_404(Category, slug=taxonomy_slug)
            c = Category.objects.all().exclude(num_products=0)
            p = Product.objects.filter(category=post)
            pro = list(p.values())
            brands  = []
            for i in range(len(pro)):
                brands.append(pro[i]['brand_id'])
            min_value = Product.objects.filter(category=post).aggregate(Min('price'))['price__min']
            max_value = Product.objects.filter(category=post).aggregate(Max('price'))['price__max']
            b = Brand.objects.all().exclude(num_products=0)
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
            min_value = Product.objects.filter(brand=post).aggregate(Min('price'))['price__min']
            max_value = Product.objects.filter(brand=post).aggregate(Max('price'))['price__max']
            b = Brand.objects.all().exclude(num_products=0)
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
        userid = request.user.id
        try:
            user_profile = UserProfile.objects.get(user_id=userid, user_name=username)
        except:
            user_profile = UserProfile.objects.create(user_id=userid, user_name=username)
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
                    auth_login(request, user)
        else:
            request.session['previous_url'] = request.get_full_path()
        return redirect('login')
def cart(request):
    if request.method == 'POST':
        i = request.POST.get('id')
        a = json.dumps({i:1})
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id, user_name=request.user.username)
        except:
            user_profile = UserProfile.objects.create(user_id=request.user.id, user_name=request.user.username)
        item = Items.objects.create(item_id = a)
        user_profile.cart.add(item)
        return JsonResponse("added Successfully", safe=False, status=200)
    if request.user.is_authenticated:
        username = request.user.username
        c = Category.objects.all().exclude(num_products=0)
        b = Brand.objects.all().exclude(num_products=0)
        p = list(Product.objects.all().values())
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id, user_name=request.user.username)
        except:
            user_profile = UserProfile.objects.create(user_id=request.user.id, user_name=request.user.username)
        cart_items = user_profile.get_cart()
        item_list = cart_items.split(',')
        keys = []
        for i in item_list:
            item = json.loads(i)
            l = {}
            for key, value in item.items():
                l['id'] = key
                l['quantity'] = value
                for j in p:
                    if j['id'] == int(key):
                        l['name'] = j['name']
                        l['price'] = value * j['price']
            keys.append(l)
        title = {
            'title': 'cart',
            'c': c,
            'b': b,
            'cart_items':keys,
            'username':username
        }
        return render(request, 'cart.html', title)
    else:
        if request.COOKIES:
            user_id = request.COOKIES.get('user_id')
            if user_id:
                user = User.objects.get(pk=user_id)
                if user:
                    auth_login(request, user)
        else:
            request.session['previous_url'] = request.get_full_path()
        return redirect('login')