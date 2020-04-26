from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from main.models import Product, Cart, CartLine
from main.forms import CartLineFormSet


def add_to_cart(request):
    product = get_object_or_404(Product, pk=request.GET.get('product_id'))
    cart = request.cart

    if not request.cart:
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        cart = Cart.objects.create(user=user)
        request.session['cart_id'] = cart.id
    cartline, created = CartLine.objects.get_or_create(
        cart=cart, product=product
    )

    if not created:
        cartline.quantity +=1
        cartline.save()
    return HttpResponseRedirect(
        reverse('product', args=(product.slug,))
    )


def manage_cart(request):
    if not request.cart:
        return render(request, 'cart.html', {'formset':None})
    if request.method == 'POST':
        formset = CartLineFormSet(
            request.POST, instance=request.cart
        )
        if formset.is_valid():
            formset.save()
    else:
        formset = CartLineFormSet(
            instance=request.cart
        )
    if request.cart.is_empty():
        return render(request, 'cart.html', {'formset': None})
    return render(request, 'cart.html', {'formset':formset})
