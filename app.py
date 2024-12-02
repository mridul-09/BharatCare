from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Flask App Configuration
app = Flask(__name__)
app.secret_key = "default_fallback_key"  # Replace with a secure key for production

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
USERNAME = "mridulsrivastava101@gmail.com"
PASSWORD = "wvlm dqon uzgv vutm"  # App password from Google
ADMIN_EMAIL = "mridulsrivastava101@gmail.com"  # Admin email

# Database Initialization
def init_db():
    """Initialize the SQLite database."""
    try:
        conn = sqlite3.connect('requests.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS requests (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            email TEXT NOT NULL,
                            product TEXT NOT NULL)''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

@app.route('/')
def index():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_request():
    """Handle product request submissions."""
    try:
        # Get form data
        data = request.form
        name = data.get('name')
        email = data.get('email')
        product = data.get('product')

        # Insert into the database
        conn = sqlite3.connect('requests.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO requests (name, email, product) VALUES (?, ?, ?)", (name, email, product))
        conn.commit()

        # Send confirmation email to the client
        client_subject = "Thank You for Your Request"
        client_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2 style="color: #4CAF50;">Thank You for Your Request</h2>
            <p>Dear {name},</p>
            <p>We have received your request for the product:</p>
            <p style="font-weight: bold; font-size: 1.1em;">{product}</p>
            <p>Our team will process your request shortly. We will keep you updated on the progress.</p>
            <p>Regards,<br>BharatCare Team</p>
        </body>
        </html>
        """
        send_email(email, client_subject, client_body, is_html=True)

        # Send notification email to the admin
        admin_subject = "New Product Request Submitted"
        admin_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2 style="color: #f44336;">New Product Request</h2>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Product Requested:</strong> {product}</p>
        </body>
        </html>
        """
        send_email(ADMIN_EMAIL, admin_subject, admin_body, is_html=True)

        flash("Request submitted successfully! Confirmation email sent to the client and notification sent to the admin.", "success")
    except sqlite3.Error as e:
        flash(f"Database error: {e}", "danger")
    except Exception as e:
        flash(f"Error sending email: {e}", "danger")
    finally:
        conn.close()

    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """Display the dashboard with submitted requests."""
    try:
        conn = sqlite3.connect('requests.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM requests")
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        rows = []
        flash(f"Database error: {e}", "danger")
    finally:
        conn.close()

    return render_template('dashboard.html', rows=rows)

def send_email(recipient, subject, body, is_html=False):
    """Send an email to a recipient."""
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = USERNAME
        msg['To'] = recipient
        msg['Subject'] = subject

        if is_html:
            msg.attach(MIMEText(body, 'html'))  # HTML formatted email
        else:
            msg.attach(MIMEText(body, 'plain'))  # Plain text email

        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure connection
            server.login(USERNAME, PASSWORD)
            server.sendmail(USERNAME, recipient, msg.as_string())
    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
