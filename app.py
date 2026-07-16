import os
import sys

# When running app.py directly, ensure the parent directory is on sys.path
# so package-style imports like `from grievance_system.config import Config` work.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from flask import Flask, redirect, url_for
from grievance_system.config import Config

from grievance_system.routes.auth import auth_bp
from grievance_system.routes.complaints import complaints_bp
from grievance_system.routes.admin import admin_bp
from grievance_system.routes.staff import staff_bp
from grievance_system.routes.ai_analysis import ai_bp
from grievance_system.routes.feedback import feedback_bp
from grievance_system.routes.analytics import analytics_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(complaints_bp, url_prefix='/complaints')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(staff_bp, url_prefix='/staff')
    app.register_blueprint(ai_bp, url_prefix='/ai')
    app.register_blueprint(feedback_bp, url_prefix='/feedback')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)