from products.models import UserProfile


#checks if the product is in cart or fav
def get_fav_cart(request, p):
    cart = 0
    fav = 0
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
    return cart, fav