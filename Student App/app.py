from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="mydatabase"
)

# Create a cursor to interact with the database
cursor = db.cursor(dictionary=True)

# Route for home page (index)
@app.route('/')
def index():
    return render_template('index.html')

# Route for student login
@app.route('/student_login')
def student_login():
    return render_template('student_login.html')

# Route for admin login
@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

# Route for student
@app.route('/student', methods=['POST'])
def student():
    user_id = request.form['id']
    
    # Assume user_id is a student's ID
    query = f"SELECT * FROM student WHERE id = {user_id}"
    cursor.execute(query)
    student = cursor.fetchone()
    
    if student:
        return render_template('student.html', student=student)
    else:
        return render_template('index.html', message='Student not found')

# Route for admin
@app.route('/admin', methods=['POST', 'GET'])
def admin():
    user_id = request.form['id']
    
    # Check if it's an admin login
    if user_id == 'admin':
        cursor.execute("SELECT * FROM student")
        students = cursor.fetchall()
        return render_template('admin.html', students=students)
    else:
        # Redirect to home page or handle unauthorized access
        return render_template('index.html', message='Unauthorized access')

# Route to handle adding new students by admin
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        id = int(request.form['id'])  # Convert to int if necessary
        name = request.form['name']
        marks = int(request.form['marks'])
        
        # Calculate result based on marks
        result = 'pass' if marks >= 150 else 'fail'
        
        # Insert new student into the database
        insert_query = "INSERT INTO student VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (id, name, marks, result))
        db.commit()
        
        # Fetch updated list of students
        cursor.execute("SELECT * FROM student")
        students = cursor.fetchall()
        return render_template('admin.html', students=students)
        
    return render_template('add_student.html')

# Route to handle deleting students by admin
@app.route('/delete_student', methods=['POST'])
def delete_student():
    student_id = request.form['student_id']
    
    # Delete student from the database
    delete_query = f"DELETE FROM student WHERE id = {student_id}"
    cursor.execute(delete_query)
    db.commit()
    
    # Fetch updated list of students
    cursor.execute("SELECT * FROM student")
    students = cursor.fetchall()
    return render_template('admin.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)
