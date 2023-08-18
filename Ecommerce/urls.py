from django.contrib import admin
from django.urls import path
from Ecommerce import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('contact/', views.contact,name='contact'),
    path('shop/', views.shop,name='shop'),
    path('register/', views.register_user,name='register'),
    path('profile/', views.profile,name='profile'),
    path('login/', views.login,name='login'),
    path('taxonomy/<slug:taxonomy_slug>/', views.taxonomy, name='taxonomy'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-placed/', views.order_placed, name='order-placed'),
    path('single-product/<slug:product_slug>', views.single_product, name='single-product'),
    path('checkout/paymentHandler/', views.paymentHandler, name='paymentHandler'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)