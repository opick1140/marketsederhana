from flask import Flask, render_template, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'kasir_sederhana'

# Data produk dengan gambar
products = [
    {'id': 1, 'name': 'Kopi', 'price': 10000, 'image': 'kopi.jpg'},
    {'id': 2, 'name': 'Teh', 'price': 5000, 'image': 'teh.jpg'},
    {'id': 3, 'name': 'Susu', 'price': 15000, 'image': 'susu.jpg'},
]

@app.route('/')
def index():
    cart = session.get('cart', {})
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('index.html', products=products, cart=cart, total_price=total_price)

@app.route('/add/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        else:
            cart[str(product_id)] = {'name': product['name'], 'price': product['price'], 'quantity': 1}
    session['cart'] = cart
    flash(f"{product['name']} ditambahkan ke keranjang!", "success")
    return redirect(url_for('index'))

@app.route('/remove/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        flash(f"{cart[str(product_id)]['name']} dihapus dari keranjang!", "warning")
        if cart[str(product_id)]['quantity'] > 1:
            cart[str(product_id)]['quantity'] -= 1
        else:
            del cart[str(product_id)]
    session['cart'] = cart
    return redirect(url_for('index'))

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    flash("Keranjang dikosongkan!", "danger")
    return redirect(url_for('index'))

@app.route('/checkout')
def checkout():
    session.pop('cart', None)
    flash("Pembelian berhasil! Terima kasih!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
