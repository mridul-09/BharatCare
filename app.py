from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure secret key

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
USERNAME = "mridulsrivastava101@gmail.com"  # Your email
PASSWORD = "wvlm dqon uzgv vutm"  # App password from Google

# Initialize database
def init_db():
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
    return render_template('index.html')  # Serve the HTML page

@app.route('/submit', methods=['POST'])
def submit_request():
    try:
        # Collect form data
        data = request.form
        name = data.get('name')
        email = data.get('email')
        product = data.get('product')

        # Insert the request into the database
        conn = sqlite3.connect('requests.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO requests (name, email, product) VALUES (?, ?, ?)", (name, email, product))
        conn.commit()

        # Send email notification
        subject = "Request Received"
        body = f"Hi {name},\n\nWe have received your request for the product: {product}. We'll get back to you soon.\n\nThank you!"

        # Compose email
        msg = MIMEMultipart()
        msg['From'] = USERNAME
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure connection
        server.login(USERNAME, PASSWORD)
        server.sendmail(USERNAME, email, msg.as_string())
        server.quit()

        flash("Request submitted successfully! A confirmation email has been sent.", "success")

    except sqlite3.Error as db_error:
        flash(f"Database error: {db_error}", "danger")
    except smtplib.SMTPException as smtp_error:
        flash(f"SMTP error: {smtp_error}", "danger")
    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
    finally:
        conn.close()

    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    try:
        # Fetch all requests from the database
        conn = sqlite3.connect('requests.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM requests")
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        rows = []
        flash(f"Database error: {e}", "danger")
    finally:
        conn.close()

    # Render the dashboard with the data
    return render_template('dashboard.html', rows=rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
