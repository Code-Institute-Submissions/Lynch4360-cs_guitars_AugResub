from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('cart', {})
    if not bag:
        messages.error(request, "There's nothing in your cart at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51LLwK0Kw7MIwdVaKkI3PBSRkPoKWSjYZBfwEOhJvEF5M4OLW2ODuymd5hXroytrUfTCx4lfX378ldjQFMreUs30C00PTuV6Wsn',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
