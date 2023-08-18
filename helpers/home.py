from helpers.shop import getKeysAndFav
from django.conf import settings

#prepare home page data
def prepareHomeData(user_profile, c, p, b, login):
    keys, fav = getKeysAndFav(user_profile)
    p_center, c_center, b_center = prepareCenters(p, c, b)
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
    return title

#prepare the courosal
def prepareCenters(p, c, b):
    p_center = 0
    c_center = 0
    b_center = 0
    if len(list(p.values())) > 3:
        p_center = 1
    if len(list(c.values())) > 3:
        c_center = 1
    if len(list(b.values())) > 3:
        b_center = 1
    return p_center, c_center, b_center