from django.conf import settings

def getTotalAndKeys(item_list, p):
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
    return keys, total

def prepareRazorPayClient(razorpay_client, checkout_amount, context):
    currency = 'INR'
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=checkout_amount, currency=currency, payment_capture='0'))
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymentHandler/'
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = checkout_amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    return context