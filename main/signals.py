from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from main.models import Cart, UserProfile, OrderLine, Order, CartLine
from django.contrib.auth import get_user_model

from main.models import Cart


@receiver(user_logged_in)
def merge_carts_if_found(sender, user, request, **kwargs):
    anon_cart = getattr(request, 'cart', None)
    if anon_cart:
        try:
            loggedin_cart = Cart.objects.get(
                user=user, status=Cart.OPEN
            )
            for line in anon_cart.cartline_set.all():
                line.cart = loggedin_cart
                line.save()
            anon_cart.delete()
            request.cart = loggedin_cart
        except Cart.DoesNotExist:
            anon_cart.user = user
            anon_cart.save()


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        instance.save()


@receiver(post_save, sender=OrderLine)
def orderline_to_order_status(sender, instance, **kwargs):

    if not instance.order.lines.filter(
        status__lt=OrderLine.SENT
    ).exists():

        instance.order.status = Order.DONE
        instance.order.save()


