from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('requests.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS requests (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        product TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML page

@app.route('/submit', methods=['POST'])
def submit_request():
    data = request.form
    name = data['name']
    email = data['email']
    product = data['product']

    # Insert the request into the database
    conn = sqlite3.connect('requests.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO requests (name, email, product) VALUES (?, ?, ?)", (name, email, product))
    conn.commit()
    conn.close()

    return render_template('success.html', message="Request submitted successfully!")

@app.route('/dashboard')
def dashboard():
    # Fetch all requests from the database
    conn = sqlite3.connect('requests.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests")
    rows = cursor.fetchall()
    conn.close()

    # Render the dashboard with the data
    return render_template('dashboard.html', rows=rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
