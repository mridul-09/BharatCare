import sqlite3

# Path to your database file
db_path = 'requests.db'

def update_requests_table():
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Check if the column already exists
            cursor.execute("PRAGMA table_info(requests)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'user_id' not in columns:
                # Add the user_id column
                cursor.execute("ALTER TABLE requests ADD COLUMN user_id INTEGER NOT NULL DEFAULT 0")
                conn.commit()
                print("user_id column added successfully to the requests table.")
            else:
                print("user_id column already exists in the requests table.")
    except sqlite3.Error as e:
        print(f"Error updating the requests table: {e}")

if __name__ == "__main__":
    update_requests_table()
