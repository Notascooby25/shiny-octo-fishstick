from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..extensions import db
from ..models import Category
from ..forms import CategoryForm

categories_bp = Blueprint("categories", __name__, template_folder="../templates")

@categories_bp.route("/", methods=["GET"])
def list_categories():
    categories = Category.query.order_by(Category.name).all()
    return render_template("categories.html", categories=categories)

@categories_bp.route("/create", methods=["GET", "POST"])
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data.strip(),
            description=form.description.data.strip() if form.description.data else None
        )
        db.session.add(category)
        db.session.commit()
        flash("Category created.", "success")
        return redirect(url_for("categories.list_categories"))
    return render_template("categories.html", form=form, create=True)

@categories_bp.route("/<int:category_id>/edit", methods=["GET", "POST"])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data.strip()
        category.description = form.description.data.strip() if form.description.data else None
        db.session.commit()
        flash("Category updated.", "success")
        return redirect(url_for("categories.list_categories"))
    return render_template("categories.html", form=form, edit=True, category=category)

@categories_bp.route("/<int:category_id>/delete", methods=["POST"])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash("Category deleted.", "info")
    return redirect(url_for("categories.list_categories"))
