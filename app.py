from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('delivery_notes.db')
    cursor = conn.cursor()
    # Create delivery_notes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS delivery_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            delivery_date TEXT NOT NULL,
            delivery_note TEXT NOT NULL,
            item_quantity INTEGER,
            delivery_status TEXT
        )
    ''')
    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            contact_number TEXT,
            address TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Dashboard route
@app.route('/')
def dashboard():
    return render_template('index.html')

# Route for delivery note capture form
@app.route('/delverynotecapture', methods=['GET', 'POST'])
def delverynotecapture():
    if request.method == 'POST':
        # Get form data
        customer_name = request.form['customer_name']
        delivery_date = request.form['delivery_date']
        delivery_note = request.form['delivery_note']
        item_quantity = request.form['item_quantity']
        delivery_status = request.form['delivery_status']

        # Save to database
        conn = sqlite3.connect('delivery_notes.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO delivery_notes (customer_name, delivery_date, delivery_note, item_quantity, delivery_status)
            VALUES (?, ?, ?, ?, ?)
        ''', (customer_name, delivery_date, delivery_note, item_quantity, delivery_status))
        conn.commit()
        conn.close()

        return redirect(url_for('delivery_notes'))

    return render_template('delverynotecapture.html')

# Route to display delivery notes
@app.route('/delivery_notes')
def delivery_notes():
    conn = sqlite3.connect('delivery_notes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM delivery_notes')
    notes = cursor.fetchall()
    conn.close()
    return render_template('deliverynotes.html', delivery_notes=notes)

# Route for customer creation form
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        # Get form data
        customer_name = request.form['customer_name']
        contact_number = request.form['contact_number']
        address = request.form['address']

        # Save to database
        conn = sqlite3.connect('delivery_notes.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO customers (customer_name, contact_number, address)
            VALUES (?, ?, ?)
        ''', (customer_name, contact_number, address))
        conn.commit()
        conn.close()

        return redirect(url_for('add_customer'))

    return render_template('add_customer.html')

@app.route('/customers')
def customers():
    conn = sqlite3.connect('delivery_notes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customers')  # Fetch all customer data
    customers = cursor.fetchall()
    conn.close()
    return render_template('customers.html', customers=customers)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)


