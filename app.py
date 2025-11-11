from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database file
DB_FILE = 'students.json'

# Initialize database
def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump([], f)

# Read students
def read_students():
    with open(DB_FILE, 'r') as f:
        return json.load(f)

# Write students
def write_students(students):
    with open(DB_FILE, 'w') as f:
        json.dump(students, f, indent=2)

# Get all students
@app.route('/api/students', methods=['GET'])
def get_students():
    students = read_students()
    return jsonify(students), 200

# Get single student
@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    students = read_students()
    student = next((s for s in students if s['id'] == student_id), None)
    if student:
        return jsonify(student), 200
    return jsonify({'error': 'Student not found'}), 404

# Create student
@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.get_json()
    
    # Validation
    required = ['name', 'email', 'age', 'course']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    students = read_students()
    
    # Generate new ID
    new_id = max([s['id'] for s in students], default=0) + 1
    
    new_student = {
        'id': new_id,
        'name': data['name'],
        'email': data['email'],
        'age': data['age'],
        'course': data['course'],
        'created_at': datetime.now().isoformat()
    }
    
    students.append(new_student)
    write_students(students)
    
    return jsonify(new_student), 201

# Update student
@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    students = read_students()
    
    student = next((s for s in students if s['id'] == student_id), None)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    # Update fields
    student['name'] = data.get('name', student['name'])
    student['email'] = data.get('email', student['email'])
    student['age'] = data.get('age', student['age'])
    student['course'] = data.get('course', student['course'])
    student['updated_at'] = datetime.now().isoformat()
    
    write_students(students)
    return jsonify(student), 200

# Delete student
@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    students = read_students()
    student = next((s for s in students if s['id'] == student_id), None)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    students = [s for s in students if s['id'] != student_id]
    write_students(students)
    
    return jsonify({'message': 'Student deleted successfully'}), 200

# Search students
@app.route('/api/students/search', methods=['GET'])
def search_students():
    query = request.args.get('q', '').lower()
    students = read_students()
    
    results = [s for s in students if 
               query in s['name'].lower() or 
               query in s['email'].lower() or 
               query in s['course'].lower()]
    
    return jsonify(results), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)