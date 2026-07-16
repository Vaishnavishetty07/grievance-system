from flask import Blueprint, request, session, redirect, url_for, render_template, flash

from grievance_system.models.complaint import Complaint
from grievance_system.models.activity_log import ActivityLog

from grievance_system.services.gemini_service import analyze_complaint
from grievance_system.services.supabase_client import supabase

import uuid
complaints_bp = Blueprint('complaints', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@complaints_bp.route('/dashboard')
@login_required
def dashboard():
    complaints = Complaint.get_by_student(session['user_id'])
    return render_template('student/dashboard.html', complaints=complaints)

@complaints_bp.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    if request.method == 'POST':
        title       = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()

        if not title or not description:
            flash('Title and description are required.', 'danger')
            return redirect(url_for('complaints.submit'))

        # Gemini AI analysis
        ai_result = analyze_complaint(title, description)

        # Image upload to Supabase Storage
        image_url = ''
        if 'image' in request.files:
            img = request.files['image']
            if img and img.filename != '':
                try:
                    ext      = img.filename.rsplit('.', 1)[-1].lower()
                    filename = f"{uuid.uuid4()}.{ext}"
                    path     = f"complaints/{filename}"
                    img_bytes = img.read()
                    supabase.storage.from_('complaint-images').upload(
                        path, img_bytes,
                        file_options={"content-type": img.content_type}
                    )
                    image_url = supabase.storage.from_('complaint-images').get_public_url(path)
                except Exception as e:
                    print(f"Image upload error: {e}")

        result = Complaint.create(
            title=title,
            description=description,
            category=ai_result.get('category', 'Other'),
            priority=ai_result.get('priority', 'Low'),
            summary=ai_result.get('summary', ''),
            image_url=image_url,
            student_id=session['user_id']
        )

        if result and result.data:
            complaint_id = result.data[0]['id']
            ActivityLog.record(complaint_id, 'Complaint submitted by student', session['user_id'])
            flash('Complaint submitted successfully!', 'success')
        else:
            flash('Error submitting complaint. Try again.', 'danger')

        return redirect(url_for('complaints.dashboard'))

    return render_template('student/submit_complaint.html')

@complaints_bp.route('/<int:complaint_id>')
@login_required
def view(complaint_id):
    complaint = Complaint.get_by_id(complaint_id)
    if not complaint:
        flash('Complaint not found.', 'danger')
        return redirect(url_for('complaints.dashboard'))
    logs = ActivityLog.get_by_complaint(complaint_id)
    return render_template('student/view_complaint.html', complaint=complaint, logs=logs)