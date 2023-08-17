from django.http import JsonResponse
from products.models import Items, Favourite
import json

#handles cart ajax
def handleCartRequest(request, user_profile):
    i = request.POST.get('id', None)
    add = request.POST.get('dict', None)
    delete = request.POST.get('delete', None)
    fav_add = request.POST.get('fav-add', None)
    fav_del = request.POST.get('fav-del', None)
    if i != None:
        return create_item(i, user_profile)
    if add != None:
        return update_item(add)
    if delete!= None:
        return delete_item(delete)
    if fav_add != None:
        return add_to_fav(fav_add, user_profile)
    if fav_del != None:
        return del_fav(fav_del)
    pass

#creates a cart item
def create_item(id, user_profile):
    item = Items.objects.create(item_id = id)
    user_profile.cart.add(item)
    return JsonResponse("added Successfully", safe=False, status=200)

#updates a cart item
def update_item(add):
    js = json.loads(add)
    for key, value in js.items():
        it = Items.objects.get(id=str(key))
        it.item_quantity = value
        it.save()
    return JsonResponse("added", safe=False, status=200)

#deletes a cart item
def delete_item(delete):
    Items.objects.get(id=str(delete)).delete()
    return JsonResponse("deleted", safe=False, status=200)

#add favourite items
def add_to_fav(fav_add, user_profile):
    fav = Favourite.objects.create(favourite_id=fav_add)
    user_profile.favourites.add(fav)
    return JsonResponse("added", safe=False, status=200)

#deletes favourite items 
def del_fav(fav_del):
    Favourite.objects.get(favourite_id=fav_del).delete()
    return JsonResponse("deleted", safe=False, status=200)
    