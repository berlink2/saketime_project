from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from main.models import Cart

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


