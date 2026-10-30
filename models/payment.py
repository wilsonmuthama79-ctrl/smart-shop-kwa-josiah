
from models import db

class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))

    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(30), nullable=False)

    transaction_code = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))

    status = db.Column(db.String(30), default="pending")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
