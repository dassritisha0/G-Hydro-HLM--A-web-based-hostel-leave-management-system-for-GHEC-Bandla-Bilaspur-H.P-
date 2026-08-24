from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), default='Caretaker') # Caretaker, Warden, or Chief Warden [cite: 84, 91, 104]

class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.String(20), unique=True, nullable=False)
    room_no = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(60), nullable=False)

class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False) # Normal, Mess-off, or Permanent [cite: 41, 92, 93]
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text, nullable=False) # [cite: 83]
    
    # Flowchart Logic: Levels of Approval [cite: 88, 100, 107]
    status_caretaker = db.Column(db.String(20), default='Pending')
    status_warden = db.Column(db.String(20), default='Pending')
    status_chief_warden = db.Column(db.String(20), default='Pending')
    final_status = db.Column(db.String(20), default='Processing')