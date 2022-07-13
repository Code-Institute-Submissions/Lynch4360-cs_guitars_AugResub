from django.shortcuts import render, redirect


def view_cart(request):
    """ A view to return the shopping cart contents """

    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """ Add an amount of a product to the shopping cart """

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
            else:
                cart[item_id]['items_by_variation'][variation] = quantity
        else:
            cart[item_id] = {'items_by_variation': {variation: quantity}}
    else:
        if item_id in list(cart.keys()):
            cart[item_id] += quantity
        else:
            cart[item_id] = quantity

    request.session['cart'] = cart
    return redirect(redirect_url)
