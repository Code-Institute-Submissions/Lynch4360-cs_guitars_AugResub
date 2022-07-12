from django.shortcuts import render

# Create your views here.

def view_cart(request):
    """ A view to return the shopping cart contents """
    
    return render(request, 'cart/cart.html')
