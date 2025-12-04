from flask import Flask, render_template, session, redirect, url_for
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Register Blueprints
from routes.auth import auth_bp
from routes.student import student_bp
from routes.warden import warden_bp

app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(warden_bp)

@app.route('/')
def index():
    if 'user_id' in session:
        if session['role'] == 'student':
            return redirect(url_for('student.dashboard'))
        else:
            return redirect(url_for('warden.dashboard'))
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)