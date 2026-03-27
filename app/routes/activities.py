from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..extensions import db
from ..models import Activity, Category
from ..forms import ActivityForm

activities_bp = Blueprint("activities", __name__, template_folder="../templates")

def _populate_category_choices(form):
    categories = Category.query.order_by(Category.name).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]

@activities_bp.route("/", methods=["GET"])
def list_activities():
    activities = Activity.query.order_by(Activity.name).all()
    return render_template("activities.html", activities=activities)

@activities_bp.route("/create", methods=["GET", "POST"])
def create_activity():
    form = ActivityForm()
    _populate_category_choices(form)
    if form.validate_on_submit():
        activity = Activity(
            name=form.name.data.strip(),
            category_id=form.category_id.data,
            is_active=form.is_active.data
        )
        db.session.add(activity)
        db.session.commit()
        flash("Activity created.", "success")
        return redirect(url_for("activities.list_activities"))
    return render_template("activities.html", form=form, create=True)

@activities_bp.route("/<int:activity_id>/edit", methods=["GET", "POST"])
def edit_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    form = ActivityForm(obj=activity)
    _populate_category_choices(form)
    if form.validate_on_submit():
        activity.name = form.name.data.strip()
        activity.category_id = form.category_id.data
        activity.is_active = form.is_active.data
        db.session.commit()
        flash("Activity updated.", "success")
        return redirect(url_for("activities.list_activities"))
    return render_template("activities.html", form=form, edit=True, activity=activity)

@activities_bp.route("/<int:activity_id>/delete", methods=["POST"])
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    db.session.delete(activity)
    db.session.commit()
    flash("Activity deleted.", "info")
    return redirect(url_for("activities.list_activities"))
