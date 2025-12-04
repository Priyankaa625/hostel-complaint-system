from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import mysql.connector
from config import Config

warden_bp = Blueprint('warden', __name__, url_prefix='/warden')

def get_db():
    return mysql.connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME
    )

def warden_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'warden':
            flash('Unauthorized access!', 'error')
            return redirect(url_for('auth.warden_login'))
        return f(*args, **kwargs)
    return decorated_function

@warden_bp.route('/dashboard')
@warden_required
def dashboard():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    # Get all complaints with user details
    cursor.execute('''
        SELECT c.*, u.username 
        FROM complaints c 
        JOIN users u ON c.user_id = u.user_id 
        ORDER BY c.created_at DESC
    ''')
    complaints = cursor.fetchall()
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) as total FROM complaints')
    total = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as pending FROM complaints WHERE status = "Pending"')
    pending = cursor.fetchone()['pending']
    
    cursor.execute('SELECT COUNT(*) as in_progress FROM complaints WHERE status = "In Progress"')
    in_progress = cursor.fetchone()['in_progress']
    
    cursor.execute('SELECT COUNT(*) as resolved FROM complaints WHERE status = "Resolved"')
    resolved = cursor.fetchone()['resolved']
    
    cursor.close()
    conn.close()
    
    return render_template('warden_dashboard.html', 
                         complaints=complaints,
                         total=total,
                         pending=pending,
                         in_progress=in_progress,
                         resolved=resolved)

@warden_bp.route('/update-status/<int:complaint_id>', methods=['POST'])
@warden_required
def update_status(complaint_id):
    new_status = request.form['status']
    
    conn = get_db()
    cursor = conn.cursor()
    
    if new_status == 'Resolved':
        cursor.execute('''
            UPDATE complaints 
            SET status = %s, resolved_at = NOW(), updated_at = NOW() 
            WHERE complaint_id = %s
        ''', (new_status, complaint_id))
    else:
        cursor.execute('''
            UPDATE complaints 
            SET status = %s, updated_at = NOW() 
            WHERE complaint_id = %s
        ''', (new_status, complaint_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash(f'Complaint #{complaint_id} updated to {new_status}!', 'success')
    return redirect(url_for('warden.dashboard'))