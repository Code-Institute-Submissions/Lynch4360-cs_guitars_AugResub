from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product

def view_cart(request):
    """ A view to return the shopping cart contents """

    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """ Add an amount of a product to the shopping cart """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    variation = None
    if 'product_variation' in request.POST:
        variation = request.POST['product_variation']
    cart = request.session.get('cart', {})

    if variation:
        if item_id in list(cart.keys()):
            if variation in cart[item_id]['items_by_variation'].keys():
                cart[item_id]['items_by_variation'][variation] += quantity
                messages.success(request, f'Updated variation {variation.upper()} {product.name} quantity to {cart[item_id]["items_by_variation"][variation]}')
            else:
                cart[item_id]['items_by_variation'][variation] = quantity
                messages.success(request, f'Added variation {variation.upper()} {product.name} to your cart')
        else:
            cart[item_id] = {'items_by_variation': {variation: quantity}}
            messages.success(request, f'Added variation {variation.upper()} {product.name} to your cart')
    else:
        if item_id in list(cart.keys()):
            cart[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {cart[item_id]}')
        else:
            cart[item_id] = quantity
            messages.success(request, f'Added {product.name} to your cart')

    request.session['cart'] = cart
    return redirect(redirect_url)


def edit_cart(request, item_id):
    """ Edit the quantity of a spedcific product in the shopping cart """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    variation = None
    if 'product_variation' in request.POST:
        variation = request.POST['product_variation']
    cart = request.session.get('cart', {})

    if variation:
        if quantity > 0:
            cart[item_id]['items_by_variation'][variation] = quantity
            messages.success(request, f'Updated variation {variation.upper()} {product.name} quantity to {cart[item_id]["items_by_variation"][variation]}')

        else:
            del cart[item_id]['items_by_variation'][variation]
            if not cart[item_id]['items_by_variation']:
                cart.pop(item_id)
                messages.success(request, f'Removed variation {variation.upper()} {product.name} to your cart')
    else:
        if quantity > 0:
            cart[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {cart[item_id]}')
        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {product.name} from your cart')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    """ Edit the quantity of a spedcific product in the shopping cart """

    try:
        product = get_object_or_404(Product, pk=item_id)
        variation = None
        if 'product_variation' in request.POST:
            variation = request.POST['product_variation']
        cart = request.session.get('cart', {})

        if variation:
            del cart[item_id]['items_by_variation'][variation]
            if not cart[item_id]['items_by_variation']:
                cart.pop(item_id)
                messages.success(request, f'Removed variation {variation.upper()} {product.name} to your cart')

        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {product.name} from your cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
