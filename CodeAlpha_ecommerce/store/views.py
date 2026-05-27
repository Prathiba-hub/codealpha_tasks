from django.shortcuts import render, redirect
from .models import Product

def product_list(request):

    products = Product.objects.all()

    return render(request, 'store/product_list.html', {
        'products': products
    })


def add_to_cart(request, product_id):

    cart = request.session.get('cart', [])

    cart.append(product_id)

    request.session['cart'] = cart

    return redirect('/cart/')


def cart(request):

    cart = request.session.get('cart', [])

    products = Product.objects.filter(id__in=cart)

    total = 0

    for product in products:
        total += product.price

    return render(request, 'store/cart.html', {
        'products': products,
        'total': total
    })

from .models import Order


def place_order(request):

    cart = request.session.get('cart', [])

    products = Product.objects.filter(id__in=cart)

    order = Order.objects.create(
        user=request.user
    )

    order.products.set(products)

    request.session['cart'] = []

    return render(request, 'store/order_success.html')