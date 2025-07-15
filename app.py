from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User
import requests
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def initialize_database():
    with app.app_context():
        db.create_all()
        if not User.query.first():
            db.session.add_all([
                User(username='admin', password=generate_password_hash('admin123')),
                User(username='ashutosh', password=generate_password_hash('ashutosh123')),
                User(username='devraj', password=generate_password_hash('devraj123')),
                User(username='yash', password=generate_password_hash('yash123'))
            ])
            db.session.commit()

initialize_database()

@app.route('/', methods=['GET'])
def home():
    if 'username' in session:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET'])
def index():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/fetch_url', methods=['GET', 'POST'])
def fetch_url():
    ssrf_info = None  
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            resp = requests.get(url)
            content = resp.text
            ssrf_info = {
                "status_code": resp.status_code,
                "headers": dict(resp.headers),
                "url": url
            }
        except Exception as e:
            content = f"Error fetching URL: {e}"
            ssrf_info = None
        return render_template('fetch_result.html', url=url, content=content, ssrf_info=ssrf_info)
    return render_template('fetch_url.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Login attempt: {username} / {password}")  # Debug
        user = User.query.filter_by(username=username).first()
        print(f"User found: {user}")  # Debug
        if user and check_password_hash(user.password, password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if 'username' not in session:
        flash('You must be logged in to reset your password.', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        if not new_password:
            flash('Password cannot be empty.', 'danger')
            return render_template('reset_password.html')
        if new_password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('reset_password.html')
        user = User.query.filter_by(username=session['username']).first()
        if user:
            user.password = generate_password_hash(new_password)
            db.session.commit()
            flash('Password reset successful! You can now log in.', 'success')
            session.pop('username', None)
            return redirect(url_for('login'))
        else:
            flash('User not found.', 'danger')
    return render_template('reset_password.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)