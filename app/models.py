from datetime import datetime
from .extensions import db

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.String(256))

    activities = db.relationship("Activity", backref="category", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category {self.name}>"

class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    logs = db.relationship("DailyLog", backref="activity", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Activity {self.name} (Category {self.category_id})>"

class DailyLog(db.Model):
    __tablename__ = "daily_logs"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, index=True)
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"), nullable=False)
    intensity = db.Column(db.Integer)
    notes = db.Column(db.String(512))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f"<DailyLog {self.date} - Activity {self.activity_id}>"
