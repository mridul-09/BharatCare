from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mail import Mail, Message
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure secret key

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'mridulsrivastava101@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'rkoi vjhl wmlm imch'  # Replace with your new app password'  # App password
app.config['MAIL_DEFAULT_SENDER'] = 'mridulsrivastava101@gmail.com'

mail = Mail(app)

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
        msg = Message(
            subject="Request Received",
            recipients=[email],  # Send to the email provided in the form
            body=f"Hi {name},\n\nWe have received your request for the product: {product}. We'll get back to you soon.\n\nThank you!"
        )
        mail.send(msg)

        flash("Request submitted successfully! A confirmation email has been sent.", "success")
    except sqlite3.Error as e:
        flash(f"Database error: {e}", "danger")
    except Exception as e:
        flash(f"Error sending email: {e}", "danger")
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
