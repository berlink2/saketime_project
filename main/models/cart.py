from django.contrib.sessions import exceptions
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from . import Product, Order, OrderLine
import logging
logger = logging.getLogger(__name__)


class Cart(models.Model):
    OPEN = 10
    SUBMITTED = 20
    STATUSES = ((OPEN, "Open"), (SUBMITTED, "Submitted"))

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True,null=True)
    status = models.IntegerField(choices=STATUSES, default=OPEN)

    def is_empty(self):
        return self.cartline_set.all().count() ==0

    def count(self):
        return sum(i.quantity for i in self.cartline_set.all())



    def create_order(self, billing_address, shipping_address):
        if not self.user:
            raise exceptions.CartException(
                "You must be logged in to submit an order."
            )
        logger.info(
            "Creating order for basket_id=%d"
            ", shipping_address_id=%d, billing_address_id=%d",
            self.id,
            shipping_address.id,
            billing_address.id,
        )
        order_data = {
            "user": self.user,
            "billing_name": billing_address.name,
            "billing_address1": billing_address.address1,
            "billing_address2": billing_address.address2,
            "billing_zip_code": billing_address.zip_code,
            "billing_city": billing_address.city,
            "billing_country": billing_address.country,
            "shipping_name": shipping_address.name,
            "shipping_address1": shipping_address.address1,
            "shipping_address2": shipping_address.address2,
            "shipping_zip_code": shipping_address.zip_code,
            "shipping_city": shipping_address.city,
            "shipping_country": shipping_address.country,
        }
        order = Order.objects.create(**order_data)
        c=0
        for line in self.cartline_set.all():
            for item in range(line.quantity):
                order_line_data = {
                    'order':order,
                    'product': line.product
                }
                order_line = OrderLine.objects.create(**order_line_data)
                c +=1
                logger.info(
                    "Created order with id=%d and lines_count=%d",
                    order.id,
                    c,
                )
        self.status = Cart.SUBMITTED
        self.save()
        return order


class CartLine(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])


