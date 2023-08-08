from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.conf import settings
from django.contrib.auth.models import User
from products.models import Category, Brand, Product, UserProfile, Items, Order, Favourite
from django.db.models import Min, Max
from django.contrib.auth.forms import UserCreationForm
import json
from datetime import datetime, timedelta
def prepare_results(request):
    results = list(Product.objects.all().values())
    keys, fav = item_list(request)
    for i in range(len(results)):
        results[i]['cart'] = 0
        results[i]['fav'] = 0
        if results[i]['id'] in keys:
            results[i]['cart'] = 1
        if results[i]['id'] in fav:
            results[i]['fav'] = 1
        category = list(Category.objects.filter(id__exact = results[i]['category_id']).values_list()[0])
        results[i]['category'] = category[1]
        brand = list(Brand.objects.filter(id__exact = results[i]['brand_id']).values_list()[0])
        results[i]['brand'] = brand[1]
    return results
def item_list(request):
    try:
        user_profile = UserProfile.objects.get(user_id=request.user.id, user_name=request.user.username)
    except:
        user_profile = UserProfile.objects.create(user_id=request.user.id, user_name=request.user.username)
    item_list = user_profile.cart.all()
    fav_items = user_profile.favourites.all()
    keys = []
    fav = []
    if len(item_list) != 0:
        for i in item_list:
            keys.append(i.item_id)
    if len(fav_items) != 0:
        for i in fav_items:
            fav.append(i.favourite_id)
    return keys, fav
def home(request):
    def login1():
        login = 1
        keys, fav = item_list(request)
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
            'fav_items':fav,
            'media_link':settings.MEDIA_URL
        }
        return render(request,'index.html',context=title)
    def login0():
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
        return login1()
        
    elif request.COOKIES:
        user_id = request.COOKIES.get('user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            if user:
                login(request, user)
                return login1()
        return login0()
                
    else:
        request.session['previous_url'] = request.get_full_path()
        return login0()
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
    def login1():
        login = 1
        c = Category.objects.all().exclude(num_products=0)
        p = Product.objects.all()
        b = Brand.objects.all().exclude(num_products=0)
        min_value = Product.objects.aggregate(Min('price'))['price__min']
        max_value = Product.objects.aggregate(Max('price'))['price__max']
        keys, fav = item_list(request)
        title = {
            'title': 'Shop',
            'c': c,
            'p': p,
            'b': b,
            'min': int(min_value),
            'max': int(max_value),
            'login': login,
            'cart_items':keys,
            'fav_items':fav,
            'media_link':settings.MEDIA_URL
        }
        return render(request,'shop.html',context=title)
    def login0():
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
    if request.method == 'POST':
        price = request.POST.get('price',0)
        brands = request.POST.getlist('brands[]')
        categories = request.POST.getlist('categories[]')
        results = prepare_results(request)
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
    if request.user.is_authenticated:
        return login1()
    elif request.COOKIES:
        user_id = request.COOKIES.get('user_id', None)
        if user_id:
            user = User.objects.get(pk=user_id)
            if user:
                auth_login(request, user)
                return login1()
        return login0()
    else:
        return login0()   
def taxonomy(request, taxonomy_slug):
    def get_category(keys,fav, login):
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
            'fav_items':fav,
            'media_link':settings.MEDIA_URL
        }
        return title
    def get_brand(keys, fav, login):
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
            'fav_items':fav,
            'media_link':settings.MEDIA_URL
        }
        return title
    def login1():
        login = 1
        keys, fav = item_list(request)
        try:
            title = get_category(keys, fav, login)
        except:
            title = get_brand(keys, fav, login)
        return render(request, 'taxonomy.html', context=title)
    def login0():
        request.session['previous_url'] = request.get_full_path()
        login = 0
        keys = []
        fav = []
        try:
            title = get_category(keys, fav, login)
        except:
            title = get_brand(keys, fav, login)
        return render(request, 'taxonomy.html', context=title)
    if request.user.is_authenticated:
        return login1()        
    elif request.COOKIES:
        user_id = request.COOKIES.get('user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            if user:
                auth_login(request, user)
                return login1()
        return login0()
    else:
        return login0()
def login_req(request):
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
    redirect('login')
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return login_req(request)
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
        return login_req(request)
    c = Category.objects.all().exclude(num_products=0)
    b = Brand.objects.all().exclude(num_products=0)
    title = {
        'title': 'Login',
        'c': c,
        'b': b,
    }
    return render(request, 'login.html', title)
def profile(request):
    def order_items(order):
        p = list(Product.objects.all().values())
        orders = []
        for i in order:
            data = {
                'id':i.id,
                'paymentStatus': i.PaymentStatus,
                'Status': i.Status,
                'Date': i.Date
            }
            order_items = []
            order_item_s = i.order_items.all()
            for j in order_item_s:
                items = {
                    'id': j.item_id,
                    'quantity': j.item_quantity
                }
                for k in p:
                    if j.item_id == k['id']:
                        items['name'] = k['name']
                order_items.append(items)
            data['order_items'] = order_items
            orders.append(data)
        print(orders)
        return orders
    def fav_items(favourites):
        p = list(Product.objects.all().values())
        favs = []
        for i in favourites:
            data = {}
            for j in p:
                if i.favourite_id == j['id']:
                    data['id'] = j['id']
                    data['price'] = j['price']
                    data['rating'] = j['rating']
                    data['pic'] = settings.MEDIA_URL + j['featured_image']
                    data['name'] = j['name']
                    data['slug'] = j['slug']
                    break
            favs.append(data)
        return favs
    if request.user.is_authenticated:
        username = request.user.username
        userid = request.user.id
        user = User.objects.get(id = userid)
        try:
            user_profile = UserProfile.objects.get(user_id=userid, user_name=username)
        except:
            user_profile = UserProfile.objects.create(user_id=userid, user_name=username)
        c = Category.objects.all().exclude(num_products=0)
        b = Brand.objects.all().exclude(num_products=0)
        orders = user_profile.orders.all()
        order_items = order_items(orders)
        favourites = user_profile.favourites.all()
        fav_items = fav_items(favourites)
        title = {
            'title': 'Profile',
            'c': c,
            'b': b,
            'orders': order_items,
            'user': user,
            'favourites':fav_items,
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
        i = request.POST.get('id', None)
        add = request.POST.get('dict', None)
        delete = request.POST.get('delete', None)
        fav_add = request.POST.get('fav-add', None)
        fav_del = request.POST.get('fav-del', None)
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id, user_name=request.user.username)
        except:
            user_profile = UserProfile.objects.create(user_id=request.user.id, user_name=request.user.username)
        if i != None:
            item = Items.objects.create(item_id = i)
            user_profile.cart.add(item)
            return JsonResponse("added Successfully", safe=False, status=200)
        if add != None:
            js = json.loads(add)
            l = []
            for key, value in js.items():
                it = Items.objects.get(id=str(key))
                it.item_quantity = value
                it.save()
            return JsonResponse("added", safe=False, status=200)
        if delete != None:
            Items.objects.get(id=str(delete)).delete()
            return JsonResponse("deleted", safe=False, status=200)
        if fav_add != None:
            fav = Favourite.objects.create(favourite_id=fav_add)
            user_profile.favourites.add(fav)
            return JsonResponse("added", safe=False, status=200)
        if fav_del != None:
            Favourite.objects.get(favourite_id=fav_del).delete()
            return JsonResponse("deleted", safe=False, status=200)
    if request.user.is_authenticated:
        username = request.user.username
        c = Category.objects.all().exclude(num_products=0)
        b = Brand.objects.all().exclude(num_products=0)
        p = list(Product.objects.all().values())
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id, user_name=request.user.username)
        except:
            user_profile = UserProfile.objects.create(user_id=request.user.id, user_name=request.user.username)
        item_list = user_profile.cart.all()
        total = 0
        keys = []
        if len(item_list) != 0:
            for i in item_list:
                l = {}
                l['id'] = i.id
                l['quantity'] = i.item_quantity
                for j in p:
                    if j['id'] == int(i.item_id):
                        l['name'] = j['name']
                        l['price'] = int(j['price'])
                        total += i.item_quantity * l['price']
                keys.append(l)
        title = {
            'title': 'Cart',
            'c': c,
            'b': b,
            'cart_items':keys,
            'total': total,
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
def checkout(request):
    if request.user.is_authenticated:
        username = request.user.username
        c = Category.objects.all().exclude(num_products=0)
        b = Brand.objects.all().exclude(num_products=0)
        p = list(Product.objects.all().values())
        user = User.objects.get(username = request.user.username)
        user_profile = UserProfile.objects.get(user_id=request.user.id, user_name=request.user.username)
        item_list = user_profile.cart.all()
        total = 0
        keys = []
        if len(item_list) != 0:
            for i in item_list:
                l = {}
                l['id'] = i.id
                l['quantity'] = i.item_quantity
                for j in p:
                    if j['id'] == int(i.item_id):
                        l['name'] = j['name']
                        l['price'] = int(j['price'])
                        total += i.item_quantity * l['price']
                keys.append(l)
        title = {
            'title': 'Checkout',
            'c': c,
            'b': b,
            'cart_items':keys,
            'total': total,
            'username':username,
            'user':user
        }
        return render(request, 'checkout.html', title)
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
def order_placed(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        firstname = request.POST.get('firstname', None)
        lastname = request.POST.get('lastname', None)
        email = request.POST.get('email',None)
        address = request.POST.get('address', None)
        payment = request.POST.get('payment', None)
        user = User.objects.get(username = request.user.username)
        user_profile = UserProfile.objects.get(user_id=request.user.id, user_name=request.user.username)
        user.username = username
        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        user.save()
        order = Order.objects.create(user_id = request.user.id, PaymentStatus = payment, Address = address)
        item_list = user_profile.cart.all()
        for i in item_list:
            order.order_items.add(i)
        user_profile.orders.add(order)
        user_profile.cart.clear()
        user_profile.save()
        return JsonResponse("added", safe=False, status= 200)
    if request.user.is_authenticated:
        username = request.user.username
        c = Category.objects.all().exclude(num_products=0)
        b = Brand.objects.all().exclude(num_products=0)
        title = {
            'title': 'Cart',
            'c': c,
            'b': b,
            'username':username,
        }
        return render(request, 'order-received.html', title)
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
def single_product(request, product_slug):
    p = Product.objects.get( slug = product_slug)
    c = Category.objects.all().exclude(num_products=0)
    b = Brand.objects.all().exclude(num_products=0)
    login = 0
    cart = 0
    fav = 0
    if request.user.is_authenticated:
        login = 1
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id, user_name=request.user.username)
        except:
            user_profile = UserProfile.objects.create(user_id=request.user.id, user_name=request.user.username)
        item_list = user_profile.cart.all()
        fav_items = user_profile.favourites.all()
        for i in item_list:
            if p.id == i.item_id:
                cart = 1
                break
        for i in fav_items:
            if p.id == i.favourite_id:
                fav = 1
    elif request.COOKIES:
        user_id = request.COOKIES.get('user_id', None)
        if user_id:
            user = User.objects.get(pk=user_id)
            if user:
                login = 1
                auth_login(request, user)
                try:
                    user_profile = UserProfile.objects.get(user_id=request.user.id, user_name=request.user.username)
                except:
                    user_profile = UserProfile.objects.create(user_id=request.user.id, user_name=request.user.username)
                item_list = user_profile.cart.all()
                fav_items = user_profile.favourites.all()
                for i in item_list:
                    if p.id == i.item_id:
                        cart = 1
                        break
                for i in fav_items:
                    if p.id == i.favourite_id:
                        fav = 1
    else:
        request.session['previous_url'] = request.get_full_path()
        login = 0
        cart = 0
    title = {
        'title':p.name,
        'c': c,
        'b': b,
        'p': p,
        'login': login,
        'cart': cart,
        'fav':fav,
        'media_link': settings.MEDIA_URL
    }
    return render(request, 'single.html', title)
    
