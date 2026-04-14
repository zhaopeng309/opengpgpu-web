from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class RoadmapForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    stage = StringField('Stage', validators=[DataRequired(), Length(max=50)])
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], default='pending')
    description = TextAreaField('Description', validators=[Optional()])
    order = IntegerField('Order', default=0)
    submit = SubmitField('Save')
