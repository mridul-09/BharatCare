from flask import Flask, request, render_template, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask App Configuration
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_fallback_key")

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
USERNAME = os.getenv("SMTP_USERNAME", "mridulsrivastava101@gmail.com")
PASSWORD = os.getenv("SMTP_PASSWORD", "wvlm dqon uzgv vutm")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "mridulsrivastava101@gmail.com")

# Database Initialization
def init_db():
    """Initialize the SQLite databases."""
    try:
        with sqlite3.connect('requests.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS requests (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                email TEXT NOT NULL,
                                product TEXT NOT NULL,
                                user_id INTEGER NOT NULL)''')
            conn.commit()

        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                email TEXT NOT NULL UNIQUE,
                                password TEXT NOT NULL)''')
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Email Sending Function
def send_email(recipient, subject, body, is_html=False):
    """Send an email to a recipient."""
    try:
        msg = MIMEMultipart()
        msg['From'] = USERNAME
        msg['To'] = recipient
        msg['Subject'] = subject
        if is_html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(USERNAME, PASSWORD)
            server.sendmail(USERNAME, recipient, msg.as_string())
    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")

# Routes
@app.route('/')
def index():
    """Render the homepage."""
    return render_template('index.html', user_logged_in=('user_id' in session))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')

            with sqlite3.connect('users.db') as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
                conn.commit()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Email already exists. Please use a different email.", "danger")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password. <a href='/register'>Unregistered user? Register here.</a>", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Log out the user."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """Display the dashboard with the user's submitted requests."""
    if 'user_id' not in session:
        flash("Please log in to view your dashboard.", "danger")
        return redirect(url_for('login'))

    user_id = session['user_id']
    with sqlite3.connect('requests.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM requests WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
    return render_template('dashboard.html', rows=rows)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Handle customer inquiries."""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        try:
            # Notify the admin via email
            admin_subject = "New Customer Inquiry"
            admin_body = f"""
            <html>
            <body>
                <h2>Customer Inquiry</h2>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Message:</strong> {message}</p>
            </body>
            </html>
            """
            send_email(ADMIN_EMAIL, admin_subject, admin_body, is_html=True)

            flash("Your message has been sent successfully!", "success")
            return redirect(url_for('contact'))
        except Exception as e:
            flash(f"Error sending your message: {e}", "danger")

    return render_template('contact.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Handle forgot password requests."""
    if request.method == 'POST':
        email = request.form['email']

        try:
            # Check if email exists in the database
            with sqlite3.connect('users.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
                user = cursor.fetchone()

            if user:
                # Generate a temporary password (for simplicity)
                temporary_password = "Temp@1234"  # Replace this with secure password generation logic
                hashed_password = generate_password_hash(temporary_password, method='pbkdf2:sha256')

                # Update the database with the temporary password
                with sqlite3.connect('users.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_password, email))
                    conn.commit()

                # Send the temporary password via email
                subject = "Password Reset Request"
                body = f"""
                <html>
                <body>
                    <p>Dear {user[1]},</p>
                    <p>We received a request to reset your password. Here is your temporary password:</p>
                    <p><strong>{temporary_password}</strong></p>
                    <p>Please log in using this temporary password and change your password immediately.</p>
                    <p>Regards,<br>BharatCare Team</p>
                </body>
                </html>
                """
                send_email(email, subject, body, is_html=True)

                flash("A temporary password has been sent to your email.", "success")
            else:
                flash("Email not found in our records. Please register first.", "danger")
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")

        return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')




if __name__ == '__main__':
    init_db()
    app.run(debug=True)
