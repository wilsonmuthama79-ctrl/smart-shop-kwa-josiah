
import os
import uuid

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from models import db
from models.product import Product, Category
from models.order import Order

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required():
    if not current_user.is_authenticated or current_user.role != "admin":
        flash("Administrator access required.", "error")
        return False
    return True


@admin_bp.route("/")
@login_required
def dashboard():
    if not admin_required():
        return redirect(url_for("auth.login"))

    return render_template(
        "admin/dashboard.html",
        product_count=Product.query.count(),
        category_count=Category.query.count(),
        order_count=Order.query.count(),
        products=Product.query.order_by(Product.id.desc()).limit(5).all()
    )


@admin_bp.route("/products")
@login_required
def products():
    if not admin_required():
        return redirect(url_for("auth.login"))

    all_products = Product.query.order_by(Product.id.desc()).all()
    return render_template("admin/products.html", products=all_products)


@admin_bp.route("/products/add", methods=["GET", "POST"])
@login_required
def add_product():
    if not admin_required():
        return redirect(url_for("auth.login"))

    categories = Category.query.order_by(Category.name).all()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        retail_price = request.form.get("retail_price", type=float)
        wholesale_price = request.form.get("wholesale_price", type=float)
        stock_quantity = request.form.get("stock_quantity", type=int)
        minimum_quantity = request.form.get("wholesale_min_quantity", type=int)
        category_id = request.form.get("category_id", type=int)

        if not name or retail_price is None or wholesale_price is None:
            flash("Please enter the product name and both prices.", "error")
            return redirect(url_for("admin.add_product"))

        if retail_price < 0 or wholesale_price < 0:
            flash("Prices cannot be negative.", "error")
            return redirect(url_for("admin.add_product"))

        if stock_quantity is None or stock_quantity < 0:
            flash("Enter a valid stock quantity.", "error")
            return redirect(url_for("admin.add_product"))

        if minimum_quantity is None or minimum_quantity < 1:
            flash("Wholesale minimum quantity must be at least 1.", "error")
            return redirect(url_for("admin.add_product"))

        category = db.session.get(Category, category_id) if category_id else None

        if category_id and not category:
            flash("Selected category does not exist.", "error")
            return redirect(url_for("admin.add_product"))

        image_name = None
        image = request.files.get("image")

        if image and image.filename:
            original_name = secure_filename(image.filename)
            extension = os.path.splitext(original_name)[1].lower()

            if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
                flash("Use JPG, JPEG, PNG or WEBP product images.", "error")
                return redirect(url_for("admin.add_product"))

            image_name = uuid.uuid4().hex + extension
            image_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"], image_name
            )
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path)

        product = Product(
            name=name,
            description=description,
            retail_price=retail_price,
            wholesale_price=wholesale_price,
            stock_quantity=stock_quantity,
            wholesale_min_quantity=minimum_quantity,
            category=category,
            image=image_name
        )

        try:
            db.session.add(product)
            db.session.commit()
            flash("Product added successfully!", "success")
            return redirect(url_for("admin.products"))
        except Exception:
            db.session.rollback()
            flash("Could not save the product. Please try again.", "error")

    return render_template("admin/add_product.html", categories=categories)

@admin_bp.route("/categories")
@login_required
def categories():
    if not admin_required():
        return redirect(url_for("auth.login"))

    all_categories = Category.query.order_by(Category.name).all()

    return render_template(
        "admin/categories.html",
        categories=all_categories
    )


@admin_bp.route("/categories/add", methods=["GET", "POST"])
@login_required
def add_category():
    if not admin_required():
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if not name:
            flash("Category name is required.", "error")
            return redirect(url_for("admin.add_category"))

        existing = Category.query.filter_by(name=name).first()

        if existing:
            flash("This category already exists.", "error")
            return redirect(url_for("admin.add_category"))

        category = Category(
            name=name,
            description=description
        )

        db.session.add(category)
        db.session.commit()

        flash("Category added successfully!", "success")
        return redirect(url_for("admin.categories"))

    return render_template("admin/add_category.html")