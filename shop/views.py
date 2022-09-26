from django.shortcuts import render
from store.models import Product
from category.models import Category

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from orders.models import Order, Payment
from .settings import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
import razorpay
from orders.constants import PaymentStatus
# import hashlib
import hmac
# import base64
# import hmac_sha256

client = razorpay.Client(
    auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


def home(request):
    print(request.path)
    products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.all()
    print(categories)
    context = {
        'products' : products[:4],
        'categories' : categories,
    }

    return render(request, 'home.html', context)


@csrf_exempt
def callback(request):
    # only accept POST request.
    if request.method == "POST":
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = client.utility.verify_payment_signature(
                params_dict)
            print(result)
           
       
            if result is not None:
                order = Order.objects.get(razorpay_order_id = razorpay_order_id)
                print(order.order_total)
                amount = int(order.order_total) * 100  # Rs. 200
                print(amount) # 30599898.0
                try:
                    # capture the payemt
                    client.payment.capture(payment_id, amount)
                    order.status = PaymentStatus.SUCCESS
                    payment = Payment(user=order.user, payment_id = payment_id, payment_method='razorpay', amount_paid = order.order_total, status=order.status)
                    payment.save()
                    order.payment = payment
                    order.razorpay_order_id = razorpay_order_id
                    order.razorpay_payment_id = payment_id
                    order.razorpay_signature_id = signature
                    order.is_ordered = True
                    order.save()

                    # render success page on successful caputre of payment
                    host = request.META['HTTP_HOST']
                    print(host)
                    redirect_url = '/orders/order_complete/'
                    print(f"'http://' + {host} + {redirect_url} + '?order_number=' + {order.order_number} + '&payment_id='+ {payment.payment_id}")
                    return HttpResponseRedirect("http://" + host + redirect_url + '?order_number=' + order.order_number + '&payment_id='+payment.payment_id)
                except:
                    order.status = PaymentStatus.FAILURE
                    print('Payment failed')
                    # if there is an error while capturing payment.
                    return render(request, 'orders/paymentfail.html')
            else:
                order.status = PaymentStatus.FAILURE
                # if signature verification fails.
                return render(request, 'orders/paymentfail.html')
 
            # if we don't find the required parameters in POST data
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
