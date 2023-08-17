from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from products.models import Category, Brand, Product, UserProfile
from django.db.models import Min, Max
from django.contrib.auth.forms import UserCreationForm
from helpers.payments import PaymentHandler, RazorPayHandler
from helpers.single_product import get_fav_cart
from helpers.checkout import getTotalAndKeys, prepareRazorPayClient
from helpers.cart import handleCartRequest
from helpers.profile import updateUserInfo, getOrdersAndFavs
from helpers.authentication import login_req
from helpers.taxonomy import get_brand, get_category
from helpers.shop import prepareShopContext, handleShopRequests, getKeysAndFav
from helpers.home import prepareHomeData
from django.core.cache import cache
global checkout_amount
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def get_category_brands():
    if cache.has_key('category'):
        cat = cache.get('categories')
    else:
        c = Category.objects.all().exclude(num_products=0)
        cache.set('categories', c, 3600)
        cat = cache.get('categories')
    if cache.has_key('brands'):
        br =  cache.get('brands')
    else:
        b = Brand.objects.all().exclude(num_products=0)
        cache.set('brands', b, 3600)
        br =  cache.get('brands')
    return cat, br


def home(request):
    c, b = get_category_brands()
    p = Product.objects.all().order_by('-rating')
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id, username=request.username)
        except:
            user_profile = None
        title = prepareHomeData(user_profile, c, p, b, 1)
    elif request.COOKIES:
        user_id = request.COOKIES.get('user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            if user:
                login(request, user)
                try:
                    user_profile = UserProfile.objects.get(user_id=request.user.id, username=request.username)
                except:
                    user_profile = None
                title = prepareHomeData(user_profile, c, p, b, 1)
            else:
                title = prepareHomeData(user_profile, c, p, b, 0)
        else:
            title = prepareHomeData(user_profile, c, p, b, 0)
    else:
        request.session['previous_url'] = request.get_full_path()
        title = prepareHomeData(user_profile, c, p, b, 0)
    return render(request,'index.html',context=title)
def contact(request):
    c, b = get_category_brands()
    title = {
        'title': 'Contact',
        'c': c,
        'b': b,
    }
    return render(request,'contact.html',context=title)
def shop(request):
    c, b = get_category_brands()
    def login1():
        login = 1
        p = Product.objects.all()
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id, user_name=request.user.username)
        except:
            user_profile = UserProfile.objects.create(user_id=request.user.id, user_name=request.user.username)
        title = prepareShopContext(user_profile, c, b, p, login)
        return render(request,'shop.html',context=title)
    def login0():
        request.session['previous_url'] = request.get_full_path()
        login = 0
        p = Product.objects.all()
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
        user_profile = None
        if request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user_id=request.user.id, username=request.username)
            except:
                user_profile = None
        return handleShopRequests(request, user_profile)
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
    c, b = get_category_brands()
    def login1():
        login = 1
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id, username=request.username)
        except:
            user_profile = None
        keys, fav = getKeysAndFav(user_profile)
        try:
            title = get_category(keys, fav, login, taxonomy_slug, c, b)
        except:
            title = get_brand(keys, fav, login, taxonomy_slug, c, b)
        return render(request, 'taxonomy.html', context=title)
    def login0():
        request.session['previous_url'] = request.get_full_path()
        login = 0
        keys = []
        fav = []
        try:
            title = get_category(keys, fav, login, taxonomy_slug, c, b)
        except:
            title = get_brand(keys, fav, login, taxonomy_slug, c, b)
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
    c, b = get_category_brands()
    title = {
        'title': 'Login',
        'c': c,
        'b': b,
    }
    return render(request, 'login.html', title)
def profile(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        updateUserInfo(request,user_profile)
    if request.user.is_authenticated:
        user = User.objects.get(id = request.user.id)
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id, user_name=request.user.username)
        except:
            user_profile = UserProfile.objects.create(user_id=request.user.id, user_name=request.user.username)
        c, b = get_category_brands()
        order_items, fav_items = getOrdersAndFavs(user_profile)
        title = {
            'title': 'Profile',
            'c': c,
            'b': b,
            'orders': order_items,
            'user': user,
            'favourites':fav_items,
            'username':request.user.username
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
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id, user_name=request.user.username)
        except:
            user_profile = UserProfile.objects.create(user_id=request.user.id, user_name=request.user.username)
        return handleCartRequest(request, user_profile)
    if request.user.is_authenticated:
        username = request.user.username
        c, b = get_category_brands()
        p = list(Product.objects.all().values())
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id, user_name=request.user.username)
        except:
            user_profile = UserProfile.objects.create(user_id=request.user.id, user_name=request.user.username)
        item_list = user_profile.cart.all()
        keys, total = getTotalAndKeys(item_list, p)
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
        c, b = get_category_brands()
        p = list(Product.objects.all().values())
        user = User.objects.get(username = request.user.username)
        user_profile = UserProfile.objects.get(user_id=request.user.id, user_name=request.user.username)
        item_list = user_profile.cart.all()
        keys, total = getTotalAndKeys(item_list, p)
        context = {
            'title': 'Checkout',
            'c': c,
            'b': b,
            'cart_items':keys,
            'total': total,
            'username':username,
            'user':user
        }
        global checkout_amount
        checkout_amount = int(total*100)
        # we need to pass these details to frontend.
        context = prepareRazorPayClient(razorpay_client, checkout_amount, context)        
        return render(request, 'checkout.html', context=context)
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
        return PaymentHandler(request)
    if request.user.is_authenticated:
        username = request.user.username
        user_profile = UserProfile.objects.get(user_id=request.user.id, user_name=request.user.username)
        c, b = get_category_brands()
        user_profile.cart.clear()
        user_profile.save()
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
    c, b = get_category_brands()
    login = 0
    cart = 0
    fav = 0
    if request.user.is_authenticated:
        login = 1
        cart, fav = get_fav_cart(request, p)
    elif request.COOKIES:
        user_id = request.COOKIES.get('user_id', None)
        if user_id:
            user = User.objects.get(pk=user_id)
            if user:
                login = 1
                auth_login(request, user)
                cart, fav = get_fav_cart(request, p)
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
    
@csrf_exempt
def paymentHandler(request):
    if request.method == 'POST':
        global checkout_amount
        return RazorPayHandler(request,razorpay_client, checkout_amount)
