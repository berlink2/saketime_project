from main.models import Cart


def cart_middleware(get_response):
    def middleware(request):
        if 'cart_id' in request.session:
            cart_id = request.session['cart_id']
            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                request.cart = None
                response = get_response(request)
                return response
            request.cart = cart
        else:
            request.cart= None
        response= get_response(request)
        return response
    return middleware

