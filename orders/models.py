from django.db import models
from accounts.models import Account
from store.models import Product
# Create your models here.
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus

class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    payment         = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user            = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    order_number    = models.CharField(max_length=40, null=False, blank=False)
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    phone           = models.CharField(max_length=15)
    email           = models.EmailField(max_length=50)
    address_line_1  = models.CharField(max_length=100)
    address_line_2  = models.CharField(max_length=100, blank=True)
    country         = models.CharField(max_length=50)
    state           = models.CharField(max_length=50)
    city            = models.CharField(max_length=50)
    order_note      = models.CharField(max_length=100, blank=True)
    order_total     = models.FloatField()
    tax             = models.FloatField()
    ip              = models.CharField(blank=True, max_length=20)
    is_ordered      = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    status          = models.CharField(_("Payment Status"),
                                default=PaymentStatus.PENDING,
                                max_length=254,
                                blank=False,
                                null=False,
                                )
    razorpay_payment_id = models.CharField(max_length=128, null=True, blank=True)
    razorpay_signature_id = models.CharField(max_length=128, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=128, null=True, blank=True)

    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return f"{self.id}-{self.first_name}-{self.status}"
    


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(
    Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
