from django.http import JsonResponse
from django.conf import settings

#updates user info
def updateUserInfo(request, user):
    username = request.POST.get('username', None)
    firstname = request.POST.get('firstname', None)
    lastname = request.POST.get('lastname', None)
    email = request.POST.get('email', None)
    if username != None and username != '':
        user.username = username
    if firstname != None and firstname != '':
        user.first_name = firstname
    if lastname != None and lastname != '':
        user.last_name = lastname
    if email != None and email != '':
        user.email = email
    user.save()
    return JsonResponse('added', safe=False, status=200)

#get orders and fav items of the user
def getOrdersAndFavs(user_profile, p):
    orders = user_profile.orders.all()
    order_items = get_order_items(orders, p)
    favourites = user_profile.favourites.all()
    fav_items = get_fav_items(favourites, p)
    return order_items, fav_items

#gets user orders
def get_order_items(order, p):
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
    return orders


#gets users favourites
def get_fav_items(favourites, p):
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