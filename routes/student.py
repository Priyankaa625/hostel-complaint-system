from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from config import Config
from ml.predict import predict_category_and_priority

student_bp = Blueprint('student', __name__, url_prefix='/student')

def get_db():
    return mysql.connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME
    )

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'student':
            flash('Please login first!', 'error')
            return redirect(url_for('auth.student_login'))
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    # Get student's complaints
    cursor.execute('''
        SELECT * FROM complaints 
        WHERE user_id = %s 
        ORDER BY created_at DESC
    ''', (session['user_id'],))
    complaints = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('student_dashboard.html', complaints=complaints)

@student_bp.route('/register-complaint', methods=['POST'])
@login_required
def register_complaint():
    room = request.form['room']
    category = request.form['category']
    description = request.form['description']
    
    # ML Prediction for category and priority
    predicted_category, priority = predict_category_and_priority(description)
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO complaints (user_id, room_number, category, description, predicted_category, priority, status) 
        VALUES (%s, %s, %s, %s, %s, %s, 'Pending')
    ''', (session['user_id'], room, category, description, predicted_category, priority))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Complaint registered successfully!', 'success')
    return redirect(url_for('student.dashboard'))