from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from grievance_system.models.complaint import Complaint
from grievance_system.models.user import User
from grievance_system.models.activity_log import ActivityLog
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'Admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    complaints = Complaint.get_all()
    staff_list = User.get_all_staff()
    return render_template('admin/dashboard.html', complaints=complaints, staff_list=staff_list)

@admin_bp.route('/assign/<int:complaint_id>', methods=['POST'])
@admin_required
def assign(complaint_id):
    staff_id = request.form.get('staff_id')
    if not staff_id:
        flash('Please select a staff member.', 'danger')
        return redirect(url_for('admin.dashboard'))
    Complaint.assign_staff(complaint_id, int(staff_id))
    ActivityLog.record(complaint_id, f'Assigned to staff ID {staff_id}', session['user_id'])
    flash('Staff assigned successfully.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/update_status/<int:complaint_id>', methods=['POST'])
@admin_required
def update_status(complaint_id):
    status = request.form.get('status')
    Complaint.update_status(complaint_id, status)
    ActivityLog.record(complaint_id, f'Status updated to {status} by Admin', session['user_id'])
    flash('Status updated.', 'success')
    return redirect(url_for('admin.dashboard'))