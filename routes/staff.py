from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from grievance_system.models.complaint import Complaint
from grievance_system.models.activity_log import ActivityLog
from functools import wraps

staff_bp = Blueprint('staff', __name__)

def staff_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'Staff':
            flash('Staff access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@staff_bp.route('/dashboard')
@staff_required
def dashboard():
    complaints = Complaint.get_by_staff(session['user_id'])
    return render_template('staff/dashboard.html', complaints=complaints)

@staff_bp.route('/update/<int:complaint_id>', methods=['POST'])
@staff_required
def update(complaint_id):
    status = request.form.get('status')
    Complaint.update_status(complaint_id, status)
    ActivityLog.record(complaint_id, f'Staff updated status to {status}', session['user_id'])
    flash('Status updated successfully.', 'success')
    return redirect(url_for('staff.dashboard'))