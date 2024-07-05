from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLAlchemy part of the application instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Define the Student model
class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Float, nullable=False)

# Create the database and the database table
with app.app_context():
    db.create_all()

# Define a route to ensure the app is running
@app.route('/')
def index():
    return render_template('index.html')

# Show all records
@app.route('/students')
def get_students():
    students = Student.query.order_by(Student.student_id).all()
    return render_template('students.html', students=students)

# Create a student
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        data = request.form
        new_student = Student(
            first_name=data['first_name'],
            last_name=data['last_name'],
            dob=datetime.strptime(data['dob'], '%Y-%m-%d'),
            amount_due=data['amount_due']
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('get_students'))
    return render_template('student_form.html')

# Read a student by ID
@app.route('/student/<int:student_id>')
def get_student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student_form.html', student=student, update=True)

# Update a student by ID
@app.route('/update_student/<int:student_id>', methods=['POST'])
def update_student(student_id):
    data = request.form
    student = Student.query.get_or_404(student_id)
    student.first_name = data['first_name']
    student.last_name = data['last_name']
    student.dob = datetime.strptime(data['dob'], '%Y-%m-%d')
    student.amount_due = data['amount_due']
    db.session.commit()
    return redirect(url_for('get_students'))

# Delete a student by ID
@app.route('/student/delete/<int:student_id>')
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('get_students'))

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
