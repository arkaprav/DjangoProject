
from django.contrib.auth.models import User
from products.models import UserProfile, Order
from django.http import JsonResponse
from django.shortcuts import  redirect

#creates orders
def create_order(request, payment, address, user_profile):
    order = Order.objects.create(user_id = request.user.id, PaymentStatus = payment, Address = address)
    item_list = user_profile.cart.all()
    for i in item_list:
        order.order_items.add(i)
    request.session['recent_order'] = order.id
    user_profile.orders.add(order)
    user_profile.save()

#create parameters for razor pay payment
def RazorPayParams(request):
    payment_id = request.POST.get('razorpay_payment_id', '')
    razorpay_order_id = request.POST.get('razorpay_order_id', '')
    signature = request.POST.get('razorpay_signature', '')
    params_dict = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }
    return params_dict,payment_id

#handles payment request and creates orders on success
def PaymentHandler(request):
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
    if payment == 'razor':
        request.session['address'] = address
    else:
        create_order(request, 'cod', address, user_profile)
    return JsonResponse("added", safe=False, status= 200)

#handles Razor Pay Payment requests and create orders on success
def RazorPayHandler(request, razorpay_client, checkout_amount):
    print("GETTING PARAMS DICT ...")
    params_dict, payment_id = RazorPayParams(request)
    print("GETTING SIGNATURE VERIFICATION ...")
    result = razorpay_client.utility.verify_payment_signature(
            params_dict)
    if result is not None:
        try:
            print("CAPTURIND PAYMENT ...")
            success = razorpay_client.payment.capture(payment_id, str(int(checkout_amount)))
            if success['captured'] == True:
                print("GETTING ADDRESS ...")
                address = request.session['address']
                print("GETTING USER PROFILE ...")
                user_profile = UserProfile.objects.get(user_id=request.user.id, user_name=request.user.username)
                print("CREATING ORDER ...")
                create_order(request, 'razor', address, user_profile)
                return redirect('order-placed')
            else:
                print("ELSE ...")
                return redirect('checkout')
        except:
            print("EXCEPTION OCCURED ...")
            return redirect('checkout')
    print("RESULT IS NONE ...")
    return redirect('checkout')