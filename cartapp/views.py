from django.shortcuts import redirect, render, get_object_or_404

from ecapp.models import Products
from .models import Cart, CartItems
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Products.objects.get(id=product_id)
    print(product)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        print(cart)
    except Cart.DoesNotExist or MultipleObjectsReturned:
        print('GYTYTTY')
        cart = Cart.objects.create(cart_id=_cart_id(request))
        print(cart.cart_id)
        cart.save()
    try:
        cart_item = CartItems.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()

    except CartItems.DoesNotExist:
        cart_item = CartItems.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()
        print(cart_item.product)
    return redirect('cartapp:cart_details')


def cart_details(request, total=0, counter=0, cart_items=None):
    print("cart details")
    try:
        cart = Cart.objects.all().filter(cart_id=_cart_id(request))
        cart_items= CartItems.objects.all()
        print(cart)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter))


def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Products, id=product_id)

    cart_item = CartItems.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cartapp:cart_details')

def full_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Products, id=product_id)

    cart_item = CartItems.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cartapp:cart_details')

