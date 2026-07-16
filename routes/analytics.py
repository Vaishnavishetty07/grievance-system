from flask import Blueprint, session, redirect, url_for, render_template
from grievance_system.services.supabase_client import supabase
from functools import wraps

analytics_bp = Blueprint('analytics', __name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'Admin':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@analytics_bp.route('/dashboard')
@admin_required
def dashboard():
    try:
        result = supabase.table('complaints').select('*').execute()
        complaints = result.data if getattr(result, 'data', None) else []
    except Exception as e:
        print(f"Analytics query error: {e}")
        complaints = []

    total    = len(complaints)
    pending  = sum(1 for c in complaints if c.get('status') == 'Pending')
    progress = sum(1 for c in complaints if c.get('status') == 'In Progress')
    resolved = sum(1 for c in complaints if c.get('status') == 'Resolved')

    categories = {}
    priorities = {'Low': 0, 'Medium': 0, 'High': 0}
    for c in complaints:
        cat = c.get('category', 'Other')
        categories[cat] = categories.get(cat, 0) + 1
        pri = c.get('priority', 'Low')
        if pri in priorities:
            priorities[pri] += 1

    category_labels = list(categories.keys())
    category_counts = list(categories.values())
    priority_counts = [priorities['Low'], priorities['Medium'], priorities['High']]

    return render_template('admin/analytics.html',
        total=total, pending=pending,
        progress=progress, resolved=resolved,
        category_labels=category_labels,
        category_counts=category_counts,
        priority_counts=priority_counts
    )