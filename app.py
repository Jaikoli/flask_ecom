from flask import Flask, render_template, redirect, url_for, request, session, flash
from config import Config
from models import db, Product

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Simple cart stored in session: { product_id (str) : qty (int) }

def get_cart_items():
    cart = session.get("cart", {})
    items = []
    total = 0.0
    if not cart:
        return items, total
    ids = [int(i) for i in cart.keys()]
    prods = Product.query.filter(Product.id.in_(ids)).all()
    prod_map = {p.id: p for p in prods}
    for pid_str, qty in cart.items():
        pid = int(pid_str)
        p = prod_map.get(pid)
        if not p:
            continue
        line_total = p.price * qty
        total += line_total
        items.append({"product": p, "qty": qty, "line_total": line_total})
    return items, total

@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    p = Product.query.get_or_404(product_id)
    return render_template("product.html", product=p)

@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    product_id = request.form.get("product_id")
    qty = int(request.form.get("quantity", 1))
    cart = session.get("cart", {})
    cart[product_id] = cart.get(product_id, 0) + qty
    session["cart"] = cart
    flash("Added to cart.")
    return redirect(request.referrer or url_for("index"))

@app.route("/cart", methods=["GET", "POST"])
def cart():
    if request.method == "POST":
        # update quantities or remove
        cart = {}
        for key, value in request.form.items():
            if key.startswith("qty-"):
                pid = key.split("-", 1)[1]
                try:
                    q = int(value)
                except:
                    q = 0
                if q > 0:
                    cart[pid] = q
        session["cart"] = cart
        flash("Cart updated.")
        return redirect(url_for("cart"))
    items, total = get_cart_items()
    return render_template("cart.html", items=items, total=total)

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total = get_cart_items()
    if not items:
        flash("Your cart is empty.")
        return redirect(url_for("index"))
    if request.method == "POST":
        # Dummy checkout: clear cart and show success
        session.pop("cart", None)
        return render_template("checkout.html", success=True, total=total)
    return render_template("checkout.html", success=False, items=items, total=total)

if __name__ == "__main__":
    # For dev only. In production use a WSGI server.
    app.run(debug=True)
