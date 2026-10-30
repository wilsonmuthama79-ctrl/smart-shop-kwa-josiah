
import os
import click

from flask import Flask, render_template, send_from_directory
from config import Config
from models import db, login_manager
from models.user import User
from models.product import Product, Category
from models.order import Order, OrderItem
from models.payment import Payment

from routes.admin import admin_bp
from routes.auth import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "auth.login"

app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route("/")
def home():
    products = Product.query.filter_by(
        is_available=True
    ).order_by(Product.id.desc()).limit(12).all()

    categories = Category.query.order_by(Category.name).all()

    return render_template(
        "customer/home.html",
        products=products,
        categories=categories
    )


@app.route("/test")
def test():
    return "SMART SHOP database connection is working!"


@app.route("/uploads/products/<filename>")
def uploaded_product(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


@app.cli.command("create-admin")
def create_admin():
    """Create the first administrator account."""
    email = click.prompt("Administrator email").strip().lower()

    if User.query.filter_by(email=email).first():
        click.echo("An account with that email already exists.")
        return

    full_name = click.prompt("Administrator full name")
    phone = click.prompt("Administrator phone number")
    password = click.prompt("Administrator password", hide_input=True)
    confirm = click.prompt("Confirm password", hide_input=True)

    if password != confirm:
        click.echo("Passwords do not match.")
        return

    if len(password) < 10:
        click.echo("Use a password of at least 10 characters.")
        return

    user = User(
        full_name=full_name,
        email=email,
        phone=phone,
        role="admin"
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    click.echo("Administrator account created successfully!")


with app.app_context():
    db.create_all()
    print("SMART SHOP database tables created successfully!")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)