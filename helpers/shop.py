from django.db.models import Min, Max
from products.models import Product, Category, Brand
from django.conf import settings
from django.http import JsonResponse

#gets cart and fav items of the user
def getKeysAndFav(user_profile):
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

def prepareShopContext(user_profile, c, p, b, login):
    min_value = Product.objects.aggregate(Min('price'))['price__min']
    max_value = Product.objects.aggregate(Max('price'))['price__max']
    keys, fav = getKeysAndFav(user_profile)
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
    return title

def handleShopRequests(request, user_profile = None):
    price = request.POST.get('price',0)
    brands = request.POST.getlist('brands[]')
    categories = request.POST.getlist('categories[]')
    results = prepare_results(user_profile)
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
    
def prepare_results(user_profile=None):
    results = list(Product.objects.all().values())
    if user_profile is not None:
        keys, fav = getKeysAndFav(user_profile)
    for i in range(len(results)):
        results[i]['cart'] = 0
        results[i]['fav'] = 0
        if user_profile is not None:
            if results[i]['id'] in keys:
                results[i]['cart'] = 1
            if results[i]['id'] in fav:
                results[i]['fav'] = 1
        category = list(Category.objects.filter(id__exact = results[i]['category_id']).values_list()[0])
        results[i]['category'] = category[1]
        brand = list(Brand.objects.filter(id__exact = results[i]['brand_id']).values_list()[0])
        results[i]['brand'] = brand[1]
    return results