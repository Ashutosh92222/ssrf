from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User
import requests  # <-- Add this import

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    # Add admin and 3 users if not already present
    if not User.query.first():
        db.session.add_all([
            User(username='admin', password='adminpass'),
            User(username='alice', password='alicepass'),
            User(username='bob', password='bobpass'),
            User(username='charlie', password='charliepass')
        ])
        db.session.commit()

@app.route('/', methods=['GET'])
def index():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/fetch_url', methods=['GET', 'POST'])
def fetch_url():
    """
    SSRF DEMO: This endpoint is intentionally vulnerable!
    It fetches any URL provided by the user, with no validation.
    """
    ssrf_info = None  
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            # SSRF vulnerability: user controls the URL fetched by the server
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
        user = User.query.filter_by(username=username).first()
        # FIX: Check both username and password
        if user and user.password == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        username = request.form.get('username')
        new_password = request.form.get('new_password')
        user = User.query.filter_by(username=username).first()
        if user:
            user.password = new_password
            db.session.commit()
            flash('Password reset successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username not found.', 'danger')
    return render_template('reset_password.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)