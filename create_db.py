from flask import Flask
from config import Config
from models import db, Product

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

sample_products = [
    {"title": "Blue T-Shirt", "description": "Comfortable cotton t-shirt", "price": 349.0, "image": ""},
    {"title": "Sneakers", "description": "Lightweight running shoes", "price": 2499.0, "image": ""},
    {"title": "Earbuds", "description": "Wireless earbuds with mic", "price": 1299.0, "image": ""},
]

with app.app_context():
    db.drop_all()
    db.create_all()
    for p in sample_products:
        prod = Product(title=p["title"], description=p["description"], price=p["price"], image=p["image"])
        db.session.add(prod)
    db.session.commit()
    print("Database created with sample products.")
