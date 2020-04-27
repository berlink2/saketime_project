from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from main.models import Product, Cart, CartLine
from main.forms import CartLineFormSet
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView


def add_to_cart(request):
    product = get_object_or_404(
        Product, id=request.GET.get("product")
    )
    cart = request.cart
    if not request.cart:
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        cart = Cart.objects.create(user=user)
        request.session["cart_id"] = cart.id

    cartline, created = CartLine.objects.get_or_create(
        cart=cart, product=product
    )
    if not created:
        cartline.quantity += 1
        cartline.save()
    return HttpResponseRedirect(
        reverse("product", args=(product.slug,))
    )


def manage_cart(request):

    if not request.cart:
        return render(request, 'cart.html', {'formset':None})


    if request.method == 'POST':
        formset = CartLineFormSet(
            request.POST, instance=request.cart, prefix='cartline'
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


def add_one_to_cart(request,slug):
    product = get_object_or_404(Product, slug=slug)
    cart = request.cart
    cartline = CartLine.objects.get(cart=cart, product=product)

    if cartline:
        cartline.quantity +=1
        cartline.save()
        cart.save()

    return redirect('cart')


def remove_one_from_cart(request,slug):
    product = get_object_or_404(Product, slug=slug)
    cart = request.cart
    cartline = CartLine.objects.get(product=product, cart=cart)

    if cartline and cartline.quantity>1:
        cartline.quantity -=1
        cartline.save()
        cart.save()
    else:
        cartline.delete()
        cart.save()


    return redirect('cart')


def remove_product_from_cart(request,slug):
    product = get_object_or_404(Product, slug=slug)
    cart = request.cart
    cartline = CartLine.objects.filter(product=product, cart=cart)

    if cartline:
        cartline.delete()

    return redirect('cart')







# class CartLineDeleteView(DeleteView):
#     model = CartLine
#     success_url = reverse_lazy('cart')
#
#     def get_queryset(self):
#         return self.model.objects.filter(cart__user=self.request.user)