from flask import Blueprint, jsonify, send_file, request, redirect, url_for, flash
from ..extensions import db
from ..models import Category, Activity
import json
import io

import_export_bp = Blueprint("import_export", __name__)

@import_export_bp.route("/export", methods=["GET"])
def export_data():
    categories = Category.query.all()

    data = []
    for c in categories:
        data.append({
            "name": c.name,
            "description": c.description,
            "activities": [
                {"name": a.name, "is_active": a.is_active}
                for a in c.activities
            ]
        })

    json_bytes = json.dumps(data, indent=2).encode("utf-8")
    buffer = io.BytesIO(json_bytes)

    return send_file(
        buffer,
        mimetype="application/json",
        as_attachment=True,
        download_name="wellness_categories.json"
    )
@import_export_bp.route("/import", methods=["POST"])
def import_data():
    file = request.files.get("file")

    if not file:
        flash("No file uploaded.", "danger")
        return redirect(url_for("categories.list_categories"))

    try:
        data = json.load(file)
    except Exception:
        flash("Invalid JSON file.", "danger")
        return redirect(url_for("categories.list_categories"))

    # Optional: wipe existing
    if request.form.get("mode") == "replace":
        Activity.query.delete()
        Category.query.delete()
        db.session.commit()

    for c in data:
        category = Category.query.filter_by(name=c["name"]).first()
        if not category:
            category = Category(name=c["name"], description=c.get("description"))
            db.session.add(category)
            db.session.flush()

        for a in c.get("activities", []):
            activity = Activity.query.filter_by(
                name=a["name"], category_id=category.id
            ).first()

            if not activity:
                activity = Activity(
                    name=a["name"],
                    category_id=category.id,
                    is_active=a.get("is_active", True)
                )
                db.session.add(activity)

    db.session.commit()
    flash("Import completed successfully.", "success")
    return redirect(url_for("categories.list_categories"))
