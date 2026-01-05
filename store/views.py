from django.shortcuts import render ,redirect

# Create your views here.
from .models import Product
def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})
def add_to_cart(request, product_id):
    cart = request.session.get('cart',{})
    
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
   
    return redirect('cart_view') 
def cart_view(request):
    cart = request.session.get('cart', {})
    Product_ids = cart.keys()
    products = Product.objects.filter(id__in=Product_ids)
    cart_items = []
    total=0
    for product in products:
        quantity=cart[str(product.id)]
        subtotal=product.price * quantity
        total+=subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })
def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_view')
    Product_ids = cart.keys()
    products = Product.objects.filter(id__in=Product_ids)
    checkout_items = []
    total=0
    for product in products:
        quantity=cart[str(product.id)]
        subtotal=product.price * quantity
        total+=subtotal
        checkout_items.append({
            'products': products,
            'cart': cart,
            'total': total
        })
    return render(request, 'store/checkout.html', {
        'checkout_items': checkout_items,
        'total': total
    })
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart_view')
