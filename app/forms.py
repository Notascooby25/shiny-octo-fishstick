from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, IntegerField,
    SelectField, SelectMultipleField,
    DateField, TimeField, BooleanField, SubmitField
    
)
from wtforms.validators import Optional


class CategoryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[Optional()])
    submit = SubmitField("Save")


class ActivityForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])
    is_active = BooleanField("Active")
    submit = SubmitField("Save")


class DailyLogForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    time = TimeField("Time", validators=[DataRequired()])

    # Multi‑select for Daylio‑style logging
    activity_ids = SelectMultipleField("Activities", coerce=int, validators=[DataRequired()])

    intensity = IntegerField("Intensity (1–5)", validators=[Optional(), NumberRange(min=1, max=5)])
    notes = TextAreaField("Notes", validators=[Optional()])
    submit = SubmitField("Save")
