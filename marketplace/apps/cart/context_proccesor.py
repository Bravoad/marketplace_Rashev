from .cart import Cart


def cart_proccess(request):
    return {'cart': Cart(request)}