from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from grievance_system.models.feedback import Feedback
from grievance_system.models.complaint import Complaint
from functools import wraps

feedback_bp = Blueprint('feedback', __name__)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@feedback_bp.route('/submit/<int:complaint_id>', methods=['GET', 'POST'])
@login_required
def submit(complaint_id):
    complaint = Complaint.get_by_id(complaint_id)
    if not complaint:
        flash('Complaint not found.', 'danger')
        return redirect(url_for('complaints.dashboard'))

    if request.method == 'POST':
        rating  = int(request.form.get('rating', 3))
        comment = request.form.get('comment', '').strip()
        Feedback.create(complaint_id, rating, comment)
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('complaints.dashboard'))

    return render_template('student/feedback.html', complaint=complaint)