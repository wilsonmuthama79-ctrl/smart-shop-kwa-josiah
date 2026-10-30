
from models import db

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)

    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.id")
    )

    retail_price = db.Column(db.Float, nullable=False)
    wholesale_price = db.Column(db.Float, nullable=False)

    stock_quantity = db.Column(db.Integer, default=0)
    wholesale_min_quantity = db.Column(db.Integer, default=10)

    image = db.Column(db.String(255))
    is_available = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    category = db.relationship("Category", backref="products")
