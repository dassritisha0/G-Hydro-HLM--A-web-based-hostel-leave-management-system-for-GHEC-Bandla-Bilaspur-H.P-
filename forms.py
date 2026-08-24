from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired

class LeaveApplicationForm(FlaskForm):
    # Requirements from your synopsis and flowchart: Leave Type, Dates, and Reason
    leave_type = SelectField('Leave Type', choices=[
        ('Normal', 'Normal Leave'), 
        ('Mess off', 'Mess off'), 
        ('Permanent', 'Permanent Leave')
    ], validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    reason = TextAreaField('Reason for Leave', validators=[DataRequired()])
    submit = SubmitField('Submit Leave Request')