from django.shortcuts import render, redirect, reverse, HttpResponse


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


def edit_cart(request, item_id):
    """ Edit the quantity of a spedcific product in the shopping cart """

    quantity = int(request.POST.get('quantity'))
    variation = None
    if 'product_variation' in request.POST:
        variation = request.POST['product_variation']
    cart = request.session.get('cart', {})

    if variation:
        if quantity > 0:
            cart[item_id]['items_by_variation'][variation] = quantity
        else:
            del cart[item_id]['items_by_variation'][variation]
            if not cart[item_id]['items_by_variation']:
                cart.pop(item_id)
    else:
        if quantity > 0:
            cart[item_id] = quantity
        else:
            cart.pop(item_id)

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    """ Edit the quantity of a spedcific product in the shopping cart """

    try:
        variation = None
        if 'product_variation' in request.POST:
            variation = request.POST['product_variation']
        cart = request.session.get('cart', {})

        if variation:
            del cart[item_id]['items_by_variation'][variation]
            if not cart[item_id]['items_by_variation']:
                cart.pop(item_id)
        else:
            cart.pop(item_id)

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)

