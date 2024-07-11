# app.py

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import mysql.connector
import random
import string
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configurations
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="mydatabase"
)

cursor = db.cursor()

# Function to generate OTP
def generate_otp():
    otp = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return otp

# Function to hash passwords
def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

# Function to verify hashed password
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('ecommerce'))
    else:
        return render_template('index.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    action = request.form['action']
    email = request.form['email']
    password = request.form['password']

    if action == 'login':
        # Check if email exists
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and verify_password(password, user[2]):
            session['email'] = email  # Store email in session
            return jsonify({'redirect': url_for('ecommerce')}), 200
        
        else:
            return jsonify({'message': 'Invalid email or password!'}), 409

    elif action == 'signup':
        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'message': 'Email already exists'}), 409

        # Hash password before storing in the database
        hashed_password = hash_password(password)
        
        # Insert new user into database
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
        db.commit()

        return jsonify({'message': 'User created successfully'}), 201

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    email = request.form['email']

    # Check if email exists
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user:
        # Generate OTP
        otp = generate_otp()

        # Save OTP in session for verification
        session['otp'] = otp
        session['email'] = email

        return jsonify({'message': 'OTP for password reset is: {}'.format(otp)}), 200
    else:
        return jsonify({'message': 'Email not found in database'}), 404

@app.route('/change_password', methods=['POST'])
def change_password():
    otp_entered = request.form['otp']
    new_password = request.form['new_password']

    try:
        # Verify OTP
        if 'otp' in session and session['otp'] == otp_entered:
            email = session['email']

            # Update password in database
            hashed_password = hash_password(new_password)
            cursor.execute("UPDATE users SET password=%s WHERE email=%s", (hashed_password, email))
            db.commit()

            # Clear session variables
            session.pop('otp', None)
            session.pop('email', None)

            return jsonify({'message': 'Password changed successfully'}), 200
        else:
            return jsonify({'message': 'Invalid OTP. Please try again'}), 401
    except Exception as e:
        return jsonify({'message': 'Error changing password: {}'.format(str(e))}), 500

@app.route('/ecommerce')
def ecommerce():
    if 'email' not in session:
        return redirect(url_for('index'))

    # Fetch categories from the database
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    return render_template('ecommerce.html', categories=categories)

@app.route('/products_by_category/<int:category_id>')
def products_by_category(category_id):
    if 'email' not in session:
        return redirect(url_for('index'))

    # Fetch category name for display
    cursor.execute("SELECT name FROM categories WHERE category_id=%s", (category_id,))
    category_name = cursor.fetchone()[0]

    # Fetch products in the selected category
    cursor.execute("SELECT * FROM products WHERE category_id=%s", (category_id,))
    products = cursor.fetchall()

    return render_template('products_by_category.html', category_name=category_name, products=products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'email' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    email = session['email']
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])  # Convert quantity to integer

    # Retrieve user_id based on email
    cursor.execute("SELECT user_id FROM users WHERE email=%s", (email,))
    user_id = cursor.fetchone()[0]

    # Check if the product is already in the user's cart
    cursor.execute("SELECT * FROM user_cart WHERE user_id=%s AND product_id=%s", (user_id, product_id))
    existing_item = cursor.fetchone()

    if existing_item:
        # Update quantity if the product is already in the cart
        new_quantity = existing_item[3] + quantity  # Add to existing quantity
        cursor.execute("UPDATE user_cart SET quantity = %s WHERE cart_id=%s", (new_quantity, existing_item[0]))
        db.commit()
    else:
        # Add new item to the cart
        cursor.execute("INSERT INTO user_cart (user_id, product_id, quantity) VALUES (%s, %s, %s)", (user_id, product_id, quantity))
        db.commit()

    return jsonify({'message': 'Product added to cart'}), 200

@app.route('/update_cart', methods=['POST'])
def update_cart():
    if 'email' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    email = session['email']
    cart_id = request.form['cart_id']
    quantity = int(request.form['quantity'])

    # Retrieve user_id based on email
    cursor.execute("SELECT user_id FROM users WHERE email=%s", (email,))
    user_id = cursor.fetchone()[0]

    if quantity <= 0:
        # Remove item from cart if quantity is 0 or less
        cursor.execute("DELETE FROM user_cart WHERE cart_id=%s", (cart_id,))
    else:
        # Update quantity in the cart
        cursor.execute("UPDATE user_cart SET quantity = %s WHERE cart_id=%s AND user_id=%s", (quantity, cart_id, user_id))
    db.commit()

    return redirect(url_for('view_cart'))

@app.route("/clear_cart")
def clear_cart():
    if 'email' not in session:
        return redirect(url_for('index'))
    
    email = session['email']

    # Retrieve user_id based on email
    cursor.execute("SELECT user_id FROM users WHERE email=%s", (email,))
    user_id = cursor.fetchone()[0]
    
    cursor.execute("DELETE FROM user_cart WHERE user_id = %s", (user_id,))
    db.commit()

    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    if 'email' not in session:
        return redirect(url_for('index'))

    email = session['email']

    # Retrieve user_id based on email
    cursor.execute("SELECT user_id FROM users WHERE email=%s", (email,))
    user_id = cursor.fetchone()[0]

    # Fetch user's cart items
    cursor.execute("""
        SELECT uc.cart_id, p.product_id, p.name, p.description, p.price, p.image_url, uc.quantity
        FROM user_cart uc
        JOIN products p ON uc.product_id = p.product_id
        WHERE uc.user_id = %s
    """, (user_id,))
    cart_items = cursor.fetchall()

    return render_template('cart.html', cart_items=cart_items)

@app.route('/checkout')
def checkout():
    if 'email' not in session:
        return redirect(url_for('index'))

    email = session['email']

    # Retrieve user_id based on email
    cursor.execute("SELECT user_id FROM users WHERE email=%s", (email,))
    user_id = cursor.fetchone()[0]

    # Fetch user's cart items and calculate total cost
    cursor.execute("""
        SELECT p.name, p.price, uc.quantity
        FROM user_cart uc
        JOIN products p ON uc.product_id = p.product_id
        WHERE uc.user_id = %s
    """, (user_id,))
    cart_items = cursor.fetchall()

    total_cost = sum(item[1] * item[2] for item in cart_items)  # price * quantity

    return render_template('checkout.html', cart_items=cart_items, total_cost=total_cost)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
