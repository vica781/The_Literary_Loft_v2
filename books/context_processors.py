def cart_contents(request):
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    cart_total = sum(item['quantity'] * float(item['price']) for item in cart.values())
    return {'cart_count': cart_count, 'cart_total': cart_total}