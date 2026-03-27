from datetime import date, datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..extensions import db
from ..models import DailyLog, Activity, Category
from ..forms import DailyLogForm

logs_bp = Blueprint("logs", __name__, template_folder="../templates")


def _populate_activity_choices(form):
    activities = Activity.query.filter_by(is_active=True).order_by(Activity.name).all()
    form.activity_ids.choices = [(a.id, f"{a.name} ({a.category.name})") for a in activities]


@logs_bp.route("/", methods=["GET"])
def list_logs():
    logs = DailyLog.query.order_by(DailyLog.timestamp.desc(), DailyLog.created_at.desc()).limit(100).all()
    return render_template("logs.html", logs=logs)


@logs_bp.route("/create", methods=["GET", "POST"])
def create_log():
    form = DailyLogForm()
    _populate_activity_choices(form)

    categories = Category.query.order_by(Category.name).all()

    if request.method == "GET":
        form.date.data = date.today()
        form.time.data = datetime.now().time()

    if form.validate_on_submit():
        dt = datetime.combine(form.date.data, form.time.data)

        for activity_id in form.activity_ids.data:
            log = DailyLog(
                timestamp=dt,
                activity_id=activity_id,
                intensity=form.intensity.data,
                notes=form.notes.data.strip() if form.notes.data else None
            )
            db.session.add(log)

        db.session.commit()
        flash("Log saved.", "success")
        return redirect(url_for("logs.list_logs"))

    return render_template("logs.html", form=form, categories=categories, create=True)
