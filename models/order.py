
from models import db

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    total_amount = db.Column(db.Float, nullable=False, default=0)
    payment_method = db.Column(db.String(30))
    payment_status = db.Column(db.String(30), default="pending")
    order_status = db.Column(db.String(30), default="pending")

    delivery_address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    items = db.relationship(
        "OrderItem", backref="order", cascade="all, delete-orphan"
    )


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))

    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
