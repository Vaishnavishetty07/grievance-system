from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from grievance_system.models.user import User
import hashlib

auth_bp = Blueprint('auth', __name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'Student')
        hostel_block = request.form.get('hostel_block', '')
        room_number = request.form.get('room_number', '')

        print("\n===== REGISTRATION ATTEMPT =====")
        print("Name:", name)
        print("Email:", email)
        print("Role:", role)

        existing = User.get_by_email(email)

        if existing:
            print("User already exists!")
            flash('Email already registered. Please login.', 'danger')
            return redirect(url_for('auth.register'))

        password_hash = hash_password(password)

        print("Password Hash:", password_hash)

        result = User.create(
            name,
            email,
            password_hash,
            role,
            hostel_block,
            room_number
        )

        print("Registration Result:", result)

        if result:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Registration failed. Check terminal logs.', 'danger')

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        print("\n===== LOGIN ATTEMPT =====")
        print("Entered Email:", email)

        user = User.get_by_email(email)

        print("User Found:", user)

        if user:

            entered_hash = hash_password(password)

            print("Stored Password:", user.get('password'))
            print("Entered Hash:", entered_hash)

            if user['password'] == entered_hash:

                print("LOGIN SUCCESSFUL")

                session['user_id'] = user['id']
                session['role'] = user['role']
                session['name'] = user['name']

                if user['role'] == 'Admin':
                    return redirect(url_for('admin.dashboard'))

                elif user['role'] == 'Staff':
                    return redirect(url_for('staff.dashboard'))

                else:
                    return redirect(url_for('complaints.dashboard'))

            else:
                print("PASSWORD MISMATCH")

        else:
            print("USER NOT FOUND")

        flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))