import os
from flask import Flask, render_template, redirect, url_for, flash, request
from models import db, Student, Admin, LeaveRequest
from forms import LeaveApplicationForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_project_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hostel_leave.db'

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@app.context_processor
def inject_globals():
    return dict(site_name="Hostel Leave Management System") # Forces the name change 

@app.route('/')
def home():
    return render_template('Home.html')

# STUDENT APPLY LEAVE [cite: 55, 61]
@app.route('/apply', methods=['GET', 'POST'])
@login_required
def apply_leave():
    form = LeaveApplicationForm()
    if form.validate_on_submit():
        new_leave = LeaveRequest(
            student_id=current_user.id,
            leave_type=form.leave_type.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            reason=form.reason.data
        )
        db.session.add(new_leave)
        db.session.commit()
        flash('Request Submitted to Caretaker!', 'success')
        return redirect(url_for('home'))
    return render_template('apply_leave.html', form=form)

# ADMIN APPROVAL LOGIC (Following Flowchart) [cite: 81]
@app.route('/approve/<int:leave_id>')
@login_required
def approve_leave(leave_id):
    leave = LeaveRequest.query.get(leave_id)
    if current_user.role == 'Caretaker':
        leave.status_caretaker = 'Approved'
    elif current_user.role == 'Warden':
        leave.status_warden = 'Approved'
    elif current_user.role == 'Chief Warden':
        leave.status_chief_warden = 'Approved'
        leave.final_status = 'Accepted' # Final state in flowchart [cite: 109]
    
    db.session.commit()
    flash('Level Approved!', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Creates the functional database [cite: 48]
    app.run(debug=True, port=5051)